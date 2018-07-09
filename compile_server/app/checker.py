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

from compile_server.app.models import Resource, Example
from compile_server.app import process_handling
from compile_server.app.views import CrossDomainResponse

gnatprove_found = False
gnatemulator_found = False

ALLOW_RUNNING_PROGRAMS_EVEN_THOUGH_IT_IS_NOT_SECURE = True
# TODO: right now, executables are run through gnatemulator. We have not
# yet done the due diligence to sandbox this, though, so deactivating the
# run feature through this boolean.

ALLOWED_EXTRA_ARGS = {'spark-flow': "--mode=flow",
                      'spark-report-all': "--report=all"}
# We maintain a list of extra arguments that can be passed to the command
# line. For security we don't want the user to pass arguments as-is.


def check_gnatprove():
    """Check that gnatprove is found on the PATH"""
    # Do the check once, for performance
    global gnatprove_found
    if gnatprove_found:
        return True
    gnatprove_found = distutils.spawn.find_executable("gnatprove")
    return gnatprove_found


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
       Return the name of the directory created.
    """
    # Create a temporary directory
    tempd = tempfile.mkdtemp()

    # Copy the original resources in a sandbox directory
    for g in glob.glob(os.path.join(example.original_dir, '*')):
        if not os.path.isdir(g):
            shutil.copy(g, tempd)

    # Overwrite with the user-contributed files
    for file in received_json['files']:
        with codecs.open(os.path.join(tempd, file['basename']),
                         'w', 'utf-8') as f:
            f.write(file['contents'])

    return tempd


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

    if spark_mode:
        project_str = project_str.replace(
            "--ADC_PLACEHOLDER--",
            'for Global_Configuration_Pragmas use "spark.adc";')

    with codecs.open(project_file, "wb", encoding="utf-8") as f:
        f.write(project_str)


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

    tempd = prep_example_directory(e, received_json)

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

    # Security check

    if not ALLOW_RUNNING_PROGRAMS_EVEN_THOUGH_IT_IS_NOT_SECURE:
        return CrossDomainResponse(
           {'identifier': '',
            'message': "running programs is disabled on this server"}
        )

    # Sanity check for the existence of gnatprove

    received_json = json.loads(request.body)
    e = get_example(received_json)
    if not e:
        return CrossDomainResponse(
            {'identifier': '', 'message': "example not found"})

    tempd = prep_example_directory(e, received_json)
    main = get_main(received_json)

    if not main:
        return CrossDomainResponse(
            {'identifier': '', 'message': "main not specified"})

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
        message = "running gnatprove"

    except subprocess.CalledProcessError, exception:
        message = exception.output

    # Send the result
    result = {'identifier': os.path.basename(tempd),
              'message': message}

    return CrossDomainResponse(result)
