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

ALLOW_RUNNING_PROGRAMS_EVEN_THOUGH_IT_IS_NOT_SECURE = False
# TODO: right now, executables are run through gnatemulator. We have not
# yet done the due diligence to sandbox this, though, so deactivating the
# run feature through this boolean.


def check_gnatprove():
    """Check that gnatprove is found on the PATH"""
    # Do the check once, for performance
    global gnatprove_found
    if gnatprove_found:
        return True
    gnatprove_found = distutils.spawn.find_executable("gnatprove")
    return gnatprove_found


def check_gnatemulator():
    """Check that gnatemulator is found on the PATH"""
    # Do the check once, for performance
    global gnatemulator_found
    if gnatemulator_found:
        return True
    gnatemulator_found = distutils.spawn.find_executable("arm-eabi-gnatemu")
    return gnatemulator_found


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
        print "getting file" + str(file)
        with codecs.open(os.path.join(tempd, file['basename']),
                         'w', 'utf-8') as f:
            f.write(file['contents'])

    return tempd


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

    # Run the command(s) to check the program
    command = ["gnatprove", "-P", "main", "--checks-as-errors"]

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

    if not check_gnatemulator():
        return CrossDomainResponse({'identifier': '',
                                    'message': "gnatemulator not found"})

    received_json = json.loads(request.body)
    e = get_example(received_json)
    received_json = json.loads(request.body)

    if not e.main:
        return CrossDomainResponse(
            {'identifier': '',
             'message': "example does not have a main"})

    tempd = prep_example_directory(e, received_json)
    if not tempd:
        return CrossDomainResponse(
            {'identifier': '', 'message': "example not found"})

    # Run the command(s) to check the program
    commands = [
                ["gprbuild", "-q", "-P", "main"],
                ["arm-eabi-gnatemu", "-P", "main", e.main],
               ]

    try:
        p = process_handling.SeparateProcess(commands, tempd)
        message = "running gnatprove"

    except subprocess.CalledProcessError, exception:
        message = exception.output

    # Send the result
    result = {'identifier': os.path.basename(tempd),
              'message': message}

    return CrossDomainResponse(result)
