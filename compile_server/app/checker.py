# -*- coding: utf-8 -*-

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

gnatprove_found = False

RUNNING_PROCESSES = {}
# The currently running processes (SeparateProcess) objects, indexed by ID


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

    if identifier not in RUNNING_PROCESSES:
        # Pretend the process has finished
        return Response({'output_lines': [],
                         'status': 0,
                         'completed': True,
                         'message': "completed"})

    p = RUNNING_PROCESSES[identifier]
    lines = p.read_lines()

    # Remove some noise from the gnatprove output
    lines = [l.strip() for l in lines if not l.startswith("Summary logged")]

    returncode = p.poll()
    if returncode is None:
        # The program is still running: transmit the current lines
        return Response({'output_lines': lines,
                         'status': 0,
                         'completed': False,
                         'message': "running"})

    else:
        # The program has finished
        del(RUNNING_PROCESSES[identifier])
        return Response({'output_lines': lines,
                         'status': returncode,
                         'completed': True,
                         'message': "completed"})


@api_view(['POST'])
def check_program(request):

    # Sanity check for the existence of gnatprove

    if not check_gnatprove():
        result = {'identifier': '',
                  'message': "error"}

        return Response(result)

    received_json = json.loads(request.body)

    matches = Example.objects.filter(name=received_json['example_name'])

    if not matches:
        return Response()

    e = matches[0]

    # Create a temporary directory
    tempd = tempfile.mkdtemp()
    identifier = os.path.basename(tempd)

    # Copy the original resources in a sandbox directory
    target = os.path.join(tempd, os.path.basename(e.original_dir))
    shutil.copytree(e.original_dir, target)

    # Overwrite with the user-contributed files
    for file in received_json['files']:
        with codecs.open(os.path.join(target, file['basename']),
                         'w', 'utf-8') as f:
            f.write(file['contents'])

    # Run the command(s) to check the program
    command = ["gnatprove", "-P", "main"]

    try:
        p = process_handling.SeparateProcess(command, target)
        RUNNING_PROCESSES[identifier] = p
        message = "running gnatprove"

    except subprocess.CalledProcessError, exception:
        message = exception.output

    # Send the result
    result = {'identifier': identifier,
              'message': message}

    return Response(result)
