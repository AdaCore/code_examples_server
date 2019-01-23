#!/usr/bin/env python

""" This is a standalone Python script that runs its argument
    safely in a container.

    At the moment it assumes that the container "safecontainer"
    exists and is running.
"""

import os
import time
import sys
import subprocess
import traceback

CONT = 'safecontainer'
INTERRUPT_STRING = '<interrupted>'
INTERRUPT_RETURNCODE = 124
DEBUG = False


def run(command):
    if DEBUG:
        print ">", " ".join(command)
    output = subprocess.check_output(["lxc", "exec", CONT, "--"] + command)
    if output:
        output = output.rstrip()
    if DEBUG:
            print "<", output
    return output


def safe_run(workdir, mode, main):
    def c(cl=[]):
        """Aux procedure, run the given command line and output to stdout"""
        try:
            if DEBUG:
                print "running: {}".format(cl)
            returncode = subprocess.call(cl, cwd=workdir,
                                         stdout=sys.stdout, shell=False)
            if returncode == INTERRUPT_RETURNCODE:
                print INTERRUPT_STRING
            return True
        except Exception:
            print "ERROR when running {}".format(' '.join(cl))
            traceback.print_exc()
            return False

    c(["echo"])
    try:
        if mode == "run":
            # In "run" mode, first build, and then launch the main
            if c(["gprbuild", "-q", "-P", "main"]):
                if main:
                    # We run:
                    #  - as user 'unprivileged' that has no write access
                    #  - under a timeout
                    #  - with our ld preloader to prevent forks
                    line = ['sudo', '-u', 'unprivileged', 'timeout', '10s',
                            'bash', '-c',
                            'LD_PRELOAD=/preloader.so {}'.format(
                              os.path.join(workdir, main.split('.')[0]))]
                    c(line)

    except Exception:
        traceback.print_exc()

    finally:
        if os.path.isdir(workdir):
            time.sleep(0.2)  # Time for the filesystem to sync
            c(["rm", "-rf", workdir])


if __name__ == '__main__':
    # Do not perform any sanity checking on args - this is not meant to
    # be launched interactively
    workdir = sys.argv[1]
    mode = sys.argv[2]
    main = ""
    if len(sys.argv) > 3:
        main = sys.argv[3]

    # This is where the compiler is installed
    os.environ["PATH"] = "/gnat/bin:{}".format(os.environ["PATH"])

    safe_run(workdir, mode, main)
