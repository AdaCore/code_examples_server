#!/usr/bin/env python

""" This is a standalone Python script that runs its argument
    safely in a container.

    At the moment it assumes that the container "safecontainer"
    exists and is running.
"""

import io
import re
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

procedure_re = re.compile("^procedure +[A-Za-z][_a-zA-Z0-9]* +is", re.MULTILINE)


def run(command):
    if DEBUG:
        print ">", " ".join(command)
    output = subprocess.check_output(["lxc", "exec", CONT, "--"] + command)
    if output:
        output = output.rstrip()
    if DEBUG:
            print "<", output
    return output


def extract_ada_main(workdir):
    """Return the main if it is found in workdir, empty string otherwise"""
    # Current heuristics for finding the main:
    # find the .adb that doesn't have a .ads.

    names = [os.path.basename(f)
             for f in glob.glob(os.path.join(workdir, "*.ad[sb]"))]
    bases = set([b[:-4] for b in names])
    mains = [b for b in bases if b + '.ads' not in names]
    if mains:
        main = mains[-1]

        # Verify that the main does indeed contain a main
        with open(os.path.join(workdir, main + '.adb'), 'rb') as fd:
            main_text = fd.read()

        if not procedure_re.findall(main_text):
            # This is not a main
            main = ''

        if DEBUG and len(mains) > 1:
            print "multiple mains found"
        return main
    else:
        if DEBUG:
            print "No main found"
        return ''


def doctor_main_gpr(tempd, spark_mode=False):
    """Doctor the main.gpr to replace the placeholder with the name of the
       main, and the .adc configuration file for SPARK.

       See template "inline_code".

       Return the name of the main that was found.
    """
    # In the temporary directory, doctor the project file to know about the
    # main.

    to_insert = ''
    languages = []
    main = ""

    # Figure out which language(s) to use
    if glob.glob(os.path.join(tempd, '*.adb')):
        languages.append('Ada')
        # Figure out which main to use
        main = extract_ada_main(tempd)

    if glob.glob(os.path.join(tempd, '*.c')):
        languages.append('C')
        # If there is C
        main = 'main.c'

    if languages:
        to_insert += ("\nfor Languages use ({});".format(
            ", ".join(['"{}"'.format(x) for x in languages])))

    if main:
        to_insert += '\nfor Main use ("{}");'.format(main)

    # Read the project file

    project_file = os.path.join(tempd, "main.gpr")
    with codecs.open(project_file, "rb", encoding="utf-8") as f:
        project_str = f.read()

    project_str = project_str.replace("--MAIN_PLACEHOLDER--", to_insert)

    with codecs.open(project_file, "wb", encoding="utf-8") as f:
        f.write(project_str)

    # Create the main.adc file
    adc_file = os.path.join(tempd, "main.adc")
    contents = COMMON_ADC
    if spark_mode:
        contents += '\n' + SPARK_ADC
    with open(adc_file, "wb") as f:
        f.write(contents)

    return main


def safe_run(workdir, mode):
    def c(cl=[]):
        """Aux procedure, run the given command line and output to stdout"""
        try:
            if DEBUG:
                print "running: {}".format(cl)
            p = subprocess.Popen(cl, cwd=workdir,
                                 stdout=subprocess.PIPE, shell=False)
            while True:
                line = p.stdout.readline().replace(workdir, '.')
                if line != '':
                    print line
                    sys.stdout.flush()
                else:
                    p.poll()
                    break

            sys.stdout.flush()
            if p.returncode == INTERRUPT_RETURNCODE:
                print INTERRUPT_STRING
            return True
        except Exception:
            print "ERROR when running {}".format(' '.join(cl))
            traceback.print_exc()
            return False

    c(["echo"])
    try:
        if mode == "run":
            main = doctor_main_gpr(workdir, False)

            # In "run" mode, first build, and then launch the main
            if c(["gprbuild", "-q", "-P", "main", "-gnatwa"]):
                # We run:
                #  - as user 'unprivileged' that has no write access
                #  - under a timeout
                #  - with our ld preloader to prevent forks
                if main:
                    line = ['sudo', '-u', 'unprivileged', 'timeout', '10s',
                            'bash', '-c',
                            'LD_PRELOAD=/preloader.so {}'.format(
                              os.path.join(workdir, main.split('.')[0]))]
                    c(line)

        elif mode == "prove":
            doctor_main_gpr(workdir, spark_mode=True)
            line = ["gnatprove", "-P", "main", "--checks-as-errors",
                    "--level=0", "--no-axiom-guard"]
            c(line)
        elif mode == "prove_flow":
            doctor_main_gpr(workdir, spark_mode=True)
            line = ["gnatprove", "-P", "main", "--checks-as-errors",
                    "--level=0", "--no-axiom-guard", "--mode=flow"]
            c(line)

        elif mode == "prove_report_all":
            doctor_main_gpr(workdir, spark_mode=True)
            line = ["gnatprove", "-P", "main", "--checks-as-errors",
                    "--level=0", "--no-axiom-guard", "--report=all"]
            c(line)

        else:
            print "mode not implemented"

    except Exception:
        traceback.print_exc()

    finally:
        if os.path.isdir(workdir):
            time.sleep(0.2)  # Time for the filesystem to sync
            if not DEBUG:
                c(["rm", "-rf", workdir])


if __name__ == '__main__':
    # Do not perform any sanity checking on args - this is not meant to
    # be launched interactively
    workdir = sys.argv[1]
    mode = sys.argv[2]

    # This is where the compiler is installed
    os.environ["PATH"] = "/gnat/bin:{}".format(os.environ["PATH"])

    safe_run(workdir, mode)
