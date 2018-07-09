""" This is a standalone Python script that runs its argument
    safely in a container.

    At the moment it assumes that the container "safecontainer"
    exists and is running.
"""

import os
import time
import sys
import subprocess

CONT = 'safecontainer'
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


def safe_run(main):
    # Make a temporary directory on the container
    tmpdir = run(["mktemp", "-d"])

    try:
        run(["chown", "ubuntu", tmpdir])

        # Push the executable to the container
        subprocess.check_call(["lxc", "file", "push", main,
                               # This requires the dir to end with /
                               CONT + tmpdir + os.sep])

        # TODO: rlimit?

        # Run it, printint output to stdout as we go along
        subprocess.call(["lxc", "exec", CONT, "--",
                         "su", "ubuntu", "-c",
                         os.path.join(tmpdir, os.path.basename(main))],
                        stdout=sys.stdout)
    except E:
        print sys.exc_info()

    finally:
        if tmpdir and tmpdir.startswith("/tmp"):
            time.sleep(0.2)  # Time for the filesystem to sync
            run(["rm", "-rf", tmpdir])


if __name__ == '__main__':
    # Do not perform any sanity checking on args - this is not meant to
    # be launched interactively
    main = sys.argv[1]
    safe_run(main)
