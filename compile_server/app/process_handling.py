# This package contains two classes that can be used to launch processes
# and process their output.
#
# SeparateProcess is used to launch a series of processes: for each instance,
# a task is created to monitor the output of the processes.
#
# ProcessReader is used to read the current status of a process.
#
# The code expects that the client will make regular calls to
# ProcessReader.poll() until the processes are completed.

import os
import shutil
import sys
import subprocess
import time
import psutil
from threading import Thread
from Queue import Queue, Empty
from compile_server.app.models import ProgramRun


TIMEOUT_SECONDS = 30
# Number of seconds to allow to a process


class SeparateProcess(object):

    def __init__(self, cmd_lines, cwd):
        """Launch the given command lines in sequence in the background.
           cmd_lines is a list of lists representing the command lines
           to launch.
           cwd is a directory in which the command line is run; this directory
           is erased when the processes are finished.
        """
        self.cmd_lines = cmd_lines
        self.q = Queue()
        self.working_dir = cwd
        self.interrupted = False  # Whether we interrupted forcefully
        self.output_file = os.path.join(self.working_dir, 'output.txt')
        self.status_file = os.path.join(self.working_dir, 'status.txt')
        with open(self.status_file, 'wb') as f:
            f.write("")
        self.p = None            # the current running process
        self.time = time.time()  # the start time of the running process
        self.processes_running = True

        t = Thread(target=self._enqueue_output)
        t.daemon = True
        t.start()

        t2 = Thread(target=self._monitor_timeout)
        t2.daemon = True
        t2.start()

    def _monitor_timeout(self):
        """Monitor the running process, interrupting it if it takes too long"""

        while self.processes_running:
            if time.time() - self.time > TIMEOUT_SECONDS:
                self.interrupted = True
                with open(self.output_file, 'ab') as f:
                    f.write("<interrupted after timeout>")
                with open(self.status_file, 'wb') as f:
                    f.write("-1")
                # The current process took too long, kill it, first with
                # sigabort, then with sigkill
                try:
                    self.p.kill()
                    time.sleep(0.01)
                    os.kill(self.p.pid, 9)
                except OSError:
                    pass
                return

            time.sleep(1.0)

    def _enqueue_output(self):
        """The function that reads the output from the process"""

        # Launch each process in sequence, in the same task
        for cmd in self.cmd_lines:
            self.time = time.time()
            self.p = subprocess.Popen(
                cmd,
                cwd=self.working_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=1,
                close_fds=True)

            # Write the output line by line in the output file
            for line in iter(self.p.stdout.readline, b''):
                if self.interrupted:
                    return
                with open(self.output_file, 'ab') as f:
                    f.write(line)

            # Write the return code
            self.p.wait()
            returncode = self.p.returncode

            # Cleanup
            self.p.stdout.close()

            # If the process returned nonzero, do not run the next process
            if returncode != 0:
                break

        # Write the last return code in the status file
        with open(self.status_file, 'wb') as f:
            f.write(str(returncode))

        # When we have finished running processes, the monitor task should
        # stop
        self.processes_running = False


class ProcessReader(object):

    def __init__(self, working_dir):
        self.working_dir = working_dir
        self.output_file = os.path.join(self.working_dir, 'output.txt')
        self.status_file = os.path.join(self.working_dir, 'status.txt')

    def poll(self):
        """ Check whether the process is still running.
            return None if the process is still running, otherwise return
            the status code.
        """
        # Custom debug codes, to debug application
        if not os.path.isdir(self.working_dir):
            return 101

        if not os.path.isfile(self.status_file):
            return None

        with open(self.status_file) as f:
            status_text = f.read().strip()

        if not status_text:
            return None
        else:
            # When all the processes are completed, remove the working dir
            shutil.rmtree(self.working_dir)
            return int(status_text)

    def read_lines(self, already_read=0):
        """Read all the available lines from the process.
           already_read indicates the number of lines that have already been
           read by the process.
           Return an empty list if there is nothing to read.
        """

        # Custom debug codes, to debug application
        if not os.path.isdir(self.working_dir):
            return 103

        if not os.path.isfile(self.output_file):
            return []

        with open(self.output_file, "rb") as f:
            lines = f.readlines()

        return lines[already_read:]


def cleanup_old_processes():
    """Cleanup the list of running processes"""
    for a in ProgramRun.objects.all():
        print a.timestamp, a.working_dir
        # Remove from the database all the processes where the working dir does
        # no longer exist
        if not os.path.exists(a.working_dir):
            print "deleting because dir has been cleared", a.working_dir
            a.delete()
