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

gnatprove_found = False


def check_gnatprove():
    """Check that gnatprove is found on the PATH"""
    # Do the check once, for performance
    global gnatprove_found
    if gnatprove_found:
        return True
    gnatprove_found = distutils.spawn.find_executable("gnatprove")
    return gnatprove_found


@api_view(['POST'])
def check_program(request):

    # Sanity check for the existence of gnatprove

    if not check_gnatprove():
        result = {'output_lines': ["gnatprove not found"],
                  'status': 0,
                  'message': "error"}

        return Response(result)

    received_json = json.loads(request.body)

    matches = Example.objects.filter(name=received_json['example_name'])

    if not matches:
        return Response()

    e = matches[0]

    output = ""
    status = 0
    message = "an error occurred while checking the program"

    try:
        # Create a temporary directory
        tempd = tempfile.mkdtemp()

        # Copy the original resources in a sandbox directory
        target = os.path.join(tempd, os.path.basename(e.original_dir))
        shutil.copytree(e.original_dir, target)

        # Overwrite with the user-contributed files
        for file in received_json['files']:
            with codecs.open(os.path.join(target, file['basename']),
                             'w', 'utf-8') as f:
                f.write(file['contents'])

        # TODO: find a command to just check rather than build
        command = ["gnatprove", "-P", "main"]

        # Run the command(s) to check the program
        try:
            output = subprocess.check_output(
                command,
                stderr=subprocess.STDOUT,
                cwd=target)
            message = "success"

        except subprocess.CalledProcessError, exception:
            output = exception.output
            message = "error"
            status = exception.returncode

    finally:

        # Cleanup
        shutil.rmtree(tempd)

    output_lines = []
    for l in output.splitlines():
        # Suppress some gnatprove output that's noise for this application
        if not l.startswith("Summary logged"):
            output_lines.append(l)

    # Send the result back

    result = {'output_lines': output_lines,
              'status': status,
              'message': message}

    return Response(result)
