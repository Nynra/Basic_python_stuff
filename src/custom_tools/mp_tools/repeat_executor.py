# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 18:46:59 2021.

From: https://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds
@author: baskl
"""
import threading
import time


class Repeated_timer(object):
    """Class to repeat a task every x seconds."""

    def __init__(self, interval, function, *args, **kwargs):
        """Ïnitiate the timer."""
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.next_call = time.time()
        self.start()

    def _run(self):
        """Run the function."""
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        """Wait for the next run."""
        if not self.is_running:
            self.next_call += self.interval
            self._timer = threading.Timer(
                self.next_call - time.time(), self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        """Stop the timer."""
        self._timer.cancel()
        self.is_running = False


if __name__ == '__main__':
    from time import sleep

    def hello(name):
        """Say hello bitchesss."""
        print("Hello {}!".format(name))

    print("starting...")
    # it auto-starts, no need of rt.start()
    rt = Repeated_timer(1, hello, "World")
    try:
        sleep(10)  # your long-running job goes here...
    finally:
        rt.stop()  # end the timer
