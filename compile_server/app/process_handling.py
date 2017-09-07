import shutil
import sys
import subprocess
from threading import Thread
from Queue import Queue, Empty


class SeparateProcess(object):

    def __init__(self, cmd, cwd):
        """Launch the given command line in the background.
           cmd is a list representing the command line
           cwd is a directory in which the command line is run; this directory
           is erased when the process is finished.
        """
        self.p = subprocess.Popen(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            close_fds=True)
        self.q = Queue()
        self.working_dir = cwd
        t = Thread(target=self._enqueue_output)
        t.daemon = True
        t.start()

    def _enqueue_output(self):
        """The function that reads the output from the process"""
        for line in iter(self.p.stdout.readline, b''):
            self.q.put(line)
        self.p.stdout.close()
        shutil.rmtree(self.working_dir)

    def poll(self):
        """ Check whether the process is still running.
            return None if the process is still running, otherwise return
            the status code.
        """
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
