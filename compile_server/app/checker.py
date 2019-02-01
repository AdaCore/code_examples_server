# -*- coding: utf-8 -*-
"""
    Architecture of the server:

    --> The server (this file) collects the user input coming in from the
        website, and packages this into a directory corresponding to the
        session, for instance
            /tmp/123456

        and then launches:

             run.py <path_to_session_dir> <mode>

        This program takes care of:
            - doctoring the package according to the mode
            - transmitting it to the container
            - running the necessary commands

    On the container:
        Files:
            /gnat          <- where GNAT Community gets installed
            /workspace     <- the root of the workspaces
                /sessions  <- one directory per session, here

        Special users:
            * "unprivileged": used to run user-provided programs,
                              has write access nowhere
            * "runner": used to run programs, has write access to
                        /workspace/sessions and /tmp
"""
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


def get_example():
    """Return the example found in the received json, if any"""

    matches = Example.objects.filter(name="Inline Code")
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


@api_view(['POST'])
def check_program(request):

    # Sanity check for the existence of gnatprove

    if not check_gnatprove():
        return CrossDomainResponse(
            {'identifier': '', 'message': "gnatprove not found"})

    received_json = json.loads(request.body)
    e = get_example()
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
    received_json = json.loads(request.body)
    e = get_example()
    if not e:
        return CrossDomainResponse(
            {'identifier': '', 'message': "example not found"})

    tempd, message = prep_example_directory(e, received_json)
    if message:
        return CrossDomainResponse({'identifier': '', 'message': message})

    print received_json
    mode = received_json['mode']

    # Check whether we have too many processes running
    if not resources_available():
        return CrossDomainResponse(
            {'identifier': '',
             'message': "the machine is busy processing too many requests"})

    # Push the code to the container

    try:
        subprocess.check_call(["lxc", "file", "push", "--recursive", tempd,
                               "safecontainer/workspace/sessions/"])
        subprocess.check_call(["lxc", "exec", "safecontainer", "--",
                               "chown", "-R", "runner",
                               "/workspace/sessions/{}".format
                               (os.path.basename(tempd))])
        subprocess.check_call(["lxc", "exec", "safecontainer", "--",
                               "chmod", "-R", "a+rx",
                               "/workspace/sessions/{}".format
                               (os.path.basename(tempd))])
    except subprocess.CalledProcessError, exception:
        result = {'message': "error transferring the program"}
        return CrossDomainResponse(result)

    # Run the command(s) to check the program
    commands = [
        # Run the program
        ["lxc", "exec", "safecontainer", "--", "su", "runner",
         "-c",
         "python /workspace/run.py /workspace/sessions/{} {}".format(
            os.path.basename(tempd), mode)]
    ]

    print "\n".join(" ".join(c) for c in commands)

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
