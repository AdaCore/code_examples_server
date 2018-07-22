# -*- coding: utf-8 -*-

import glob
import os
import codecs
import distutils.spawn
import json
import shutil
import subprocess
import tempfile

from rest_framework.response import Response
from rest_framework.decorators import api_view

from compile_server.app.models import Resource, Example, ProgramRun
from compile_server.app import process_handling
from compile_server.app.views import CrossDomainResponse

gnatprove_found = False

ALLOWED_EXTRA_ARGS = {'spark-flow': "--mode=flow",
                      'spark-report-all': "--report=all"}
# We maintain a list of extra arguments that can be passed to the command
# line. For security we don't want the user to pass arguments as-is.

PROCESSES_LIMIT = 300  # The limit of processes that can be running

RECEIVED_FILE_CHAR_LIMIT = 50 * 1000
# The limit in number of characters of files to accept

COMMON_ADC = """
pragma Restrictions (No_Specification_of_Aspect => Import);
pragma Restrictions (No_Use_Of_Pragma => Import);
pragma Restrictions (No_Dependence => System.Machine_Code);
pragma Restrictions (No_Dependence => Machine_Code);
"""

SPARK_ADC = """
pragma Profile(GNAT_Extended_Ravenscar);
pragma Partition_Elaboration_Policy(Sequential);
pragma SPARK_Mode (On);
pragma Warnings (Off, "no Global contract available");
pragma Warnings (Off, "subprogram * has no effect");
pragma Warnings (Off, "file name does not match");
"""


def check_gnatprove():
    """Check that gnatprove is found on the PATH"""
    # Do the check once, for performance
    global gnatprove_found
    if gnatprove_found:
        return True
    gnatprove_found = distutils.spawn.find_executable("gnatprove")
    return gnatprove_found


def resources_available():
    """Return whether we have enough resources on the machine"""
    if len(ProgramRun.objects.all()) > PROCESSES_LIMIT:
        # We're over the limit: first attempt a cleanup
        process_handling.cleanup_old_processes()
        return len(ProgramRun.objects.all()) <= PROCESSES_LIMIT
    else:
        return True


@api_view(['POST'])
def check_output(request):
    """Check the output of a running process."""
    received_json = json.loads(request.body)
    identifier = received_json['identifier']

    p = process_handling.ProcessReader(
        os.path.join(tempfile.gettempdir(), identifier))

    print received_json['already_read']
    lines = p.read_lines(received_json['already_read'])

    # Remove some noise from the gnatprove output
    lines = [l.strip() for l in lines if not l.startswith("Summary logged")]

    returncode = p.poll()
    if returncode is None:
        # The program is still running: transmit the current lines
        return CrossDomainResponse({'output_lines': lines,
                                    'status': 0,
                                    'completed': False,
                                    'message': "running"})

    else:
        return CrossDomainResponse({'output_lines': lines,
                                    'status': returncode,
                                    'completed': True,
                                    'message': "completed"})


def get_example(received_json):
    """Return the example found in the received json, if any"""

    matches = Example.objects.filter(name=received_json['example_name'])
    if not matches:
        return None
    return matches[0]


def prep_example_directory(example, received_json):
    """Prepare the directory in which the example can be run.
       Return a tuple with
          - the name of the directory created if it exists
          - the error message if not
    """
    # Create a temporary directory
    tempd = tempfile.mkdtemp()

    # Copy the original resources in a sandbox directory
    for g in glob.glob(os.path.join(example.original_dir, '*')):
        if not os.path.isdir(g):
            shutil.copy(g, tempd)

    # Overwrite with the user-contributed files
    for file in received_json['files']:
        if len(file['contents']) > RECEIVED_FILE_CHAR_LIMIT:
            shutil.rmtree(tempd)
            return (None, "file contents exceeds size limits")
        with codecs.open(os.path.join(tempd, file['basename']),
                         'w', 'utf-8') as f:
            f.write(file['contents'])

    return (tempd, None)


def get_main(received_json):
    """Retrieve the main information from the json"""

    # Figure out which is the main
    if 'main' not in received_json:
        return None

    return received_json['main']


def doctor_main_gpr(tempd, main="", spark_mode=False):
    """Doctor the main.gpr to replace the placeholder with the name of the
       main, and the .adc configuration file for SPARK.

       See template "inline_code".
    """
    # In the temporary directory, doctor the project file to know about the
    # main.

    project_file = os.path.join(tempd, "main.gpr")
    with codecs.open(project_file, "rb", encoding="utf-8") as f:
        project_str = f.read()

    if main:
        project_str = project_str.replace(
            "--MAIN_PLACEHOLDER--",
            'for Main use ("{}");'.format(main))

    with codecs.open(project_file, "wb", encoding="utf-8") as f:
        f.write(project_str)

    # Create the main.adc file
    adc_file = os.path.join(tempd, "main.adc")
    contents = COMMON_ADC
    if spark_mode:
        contents += '\n' + SPARK_ADC
    with open(adc_file, "wb") as f:
        f.write(contents)


@api_view(['POST'])
def check_program(request):

    # Sanity check for the existence of gnatprove

    if not check_gnatprove():
        return CrossDomainResponse(
            {'identifier': '', 'message': "gnatprove not found"})

    received_json = json.loads(request.body)
    e = get_example(received_json)
    if not e:
        return CrossDomainResponse(
            {'identifier': '', 'message': "example not found"})

    # Check whether we have too many processes running
    if not resources_available():
        return CrossDomainResponse(
            {'identifier': '',
             'message': "the machine is busy processing too many requests"})

    tempd, message = prep_example_directory(e, received_json)
    if message:
        return CrossDomainResponse({'identifier': '', 'message': message})

    main = get_main(received_json)
    doctor_main_gpr(tempd, main, True)

    # Run the command(s) to check the program
    command = ["gnatprove", "-P", "main", "--checks-as-errors",
               "--level=0", "--no-axiom-guard"]

    # Process extra_args
    if 'extra_args' in received_json:
        extra_args = received_json['extra_args']
        if extra_args:
            if extra_args not in ALLOWED_EXTRA_ARGS:
                return CrossDomainResponse(
                    {'identifier': '', 'message': "extra_args not known"})
            command.append(ALLOWED_EXTRA_ARGS[extra_args])
    print " ".join(command)
    try:
        p = process_handling.SeparateProcess([command], tempd)
        message = "running gnatprove"

    except subprocess.CalledProcessError, exception:
        message = exception.output

    # Send the result
    result = {'identifier': os.path.basename(tempd),
              'message': message}

    return CrossDomainResponse(result)


@api_view(['POST'])
def run_program(request):

    # Sanity check for the existence of gnatprove

    received_json = json.loads(request.body)
    e = get_example(received_json)
    if not e:
        return CrossDomainResponse(
            {'identifier': '', 'message': "example not found"})

    tempd, message = prep_example_directory(e, received_json)
    if message:
        return CrossDomainResponse({'identifier': '', 'message': message})

    main = get_main(received_json)

    if not main:
        return CrossDomainResponse(
            {'identifier': '', 'message': "main not specified"})

    # Check whether we have too many processes running
    if not resources_available():
        return CrossDomainResponse(
            {'identifier': '',
             'message': "the machine is busy processing too many requests"})

    doctor_main_gpr(tempd, main)

    # Run the command(s) to check the program
    commands = [
                # Build the program
                ["gprbuild", "-q", "-P", "main"],
                # Launch the program via "safe_run", to sandbox it
                ["python",
                 os.path.join(os.path.dirname(__file__), 'safe_run.py'),
                 os.path.join(tempd, main[:-4])],
               ]

    print commands

    try:
        p = process_handling.SeparateProcess(commands, tempd)
        stored_run = ProgramRun(working_dir=p.working_dir)
        stored_run.save()
        message = "running gnatprove"

    except subprocess.CalledProcessError, exception:
        message = exception.output

    # Send the result
    result = {'identifier': os.path.basename(tempd),
              'message': message}

    return CrossDomainResponse(result)
