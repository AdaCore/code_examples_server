#!/usr/bin/env python

""" This is a standalone Python script that runs its argument
    safely in a container.

    At the moment it assumes that the container "safecontainer"
    exists and is running.
"""

import os
import codecs
import glob
import time
import sys
import subprocess
import traceback

CONT = 'safecontainer'
INTERRUPT_STRING = '<interrupted>'
INTERRUPT_RETURNCODE = 124
DEBUG = False


COMMON_ADC = """
pragma Restrictions (No_Specification_of_Aspect => Import);
pragma Restrictions (No_Use_Of_Pragma => Import);
pragma Restrictions (No_Use_Of_Pragma => Interface);
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


def run(command):
    if DEBUG:
        print ">", " ".join(command)
    output = subprocess.check_output(["lxc", "exec", CONT, "--"] + command)
    if output:
        output = output.rstrip()
    if DEBUG:
            print "<", output
    return output


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


def safe_run(workdir, mode):
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
            # Current heuristics for finding the main:
            # find the .adb that doesn't have a .ads.
            names = [os.path.basename(f)
                     for f in glob.glob(os.path.join(workdir, "*.ad[sb]"))]
            bases = set([b[:-4] for b in names])
            mains = [b for b in bases if b + '.ads' not in names]
            if mains:
                main = mains[-1]
                if DEBUG and len(mains) > 1:
                    print "multiple mains found"
            else:
                print "No main found"

            # Doctor the gpr to put the name of the main in there
            doctor_main_gpr(workdir, main, False)

            # In "run" mode, first build, and then launch the main
            if c(["gprbuild", "-q", "-P", "main"]):
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

    # This is where the compiler is installed
    os.environ["PATH"] = "/gnat/bin:{}".format(os.environ["PATH"])

    safe_run(workdir, mode)
