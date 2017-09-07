import shutil
import sys
import subprocess
from threading import Thread
from Queue import Queue, Empty


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
        self.p = None
        t = Thread(target=self._enqueue_output)
        t.daemon = True
        t.start()

    def _enqueue_output(self):
        """The function that reads the output from the process"""

        # Launch each process in sequence, in the same task
        for cmd in self.cmd_lines:
            self.p = subprocess.Popen(
                cmd,
                cwd=self.working_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=1,
                close_fds=True)

            for line in iter(self.p.stdout.readline, b''):
                self.q.put(line)

            self.p.stdout.close()

        # When all the processes are complete,
        shutil.rmtree(self.working_dir)

    def poll(self):
        """ Check whether the process is still running.
            return None if the process is still running, otherwise return
            the status code.
        """
        if not self.p:
            return None
        self.p.poll()
        return self.p.returncode

    def read_lines(self):
        """Read all the available lines from the process.
           Return an empty list if there"""
        lines = []
        while True:
            try:
                # Read the queue
                line = self.q.get_nowait()
                lines.append(line)
            except Empty:
                return lines
