# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 08:33:31 2022
copied from: https://stackoverflow.com/questions/19981140/clean-python-multiprocess-termination-dependant-on-an-exit-flag

@author: baskl
"""
import multiprocessing
import threading
import time


class Process_manager(object):
    """
    Class to manage processes that are prone to errors.

    When a process crashes all the other processes managed by the manager
    will be terminated cleanly.
    """

    def __init__(self):
        self.procs = []
        self.errors_flag = False
        self._threads = []
        self._lock = threading.Lock()

    def terminate_all(self):
        """Terminate all the processes that are still running"""
        with self._lock:
            for p in self.procs:
                if p.is_alive():
                    print("Terminating %s" % p)
                    p.terminate()

    def launch_proc(self, func, args=(), kwargs={}):
        """Launch a new thread to manage the process."""
        t = threading.Thread(target=self._proc_thread_runner,
                             args=(func, args, kwargs))
        self._threads.append(t)
        t.start()

    def _proc_thread_runner(self, func, args, kwargs):
        """Spawn the new process."""
        p = multiprocessing.Process(target=func, args=args, kwargs=kwargs)
        self.procs.append(p)
        p.start()
        while p.exitcode is None:
            p.join()
        if p.exitcode > 0:
            self.errors_flag = True
            self.terminate_all()
        else:
            self.procs.remove(p)

    def wait(self):
        """Wait for all the threads to finish."""
        for t in self._threads:
            t.join()


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

    ###########################
    # Process manager example #
    ###########################
    def good_worker():
        print("GoodWorker Starting")
        time.sleep(4)
        print("GoodWorker Finished")

    def bad_worker():
        print("[BadWorker] Starting")
        time.sleep(2)
        raise Exception("ups!")

    # Create the manager
    proc_manager = Process_manager()

    # Add some workers
    proc_manager.launch_proc(good_worker)
    proc_manager.launch_proc(good_worker)
    proc_manager.launch_proc(bad_worker)

    # Wait for all the workers to finish
    proc_manager.wait()

    # Check if there were errors
    if proc_manager.errors_flag:
        print("Errors flag is set: some process crashed")
    else:
        print("Everything closed cleanly")

    ###########################
    # Repeat executor example #
    ###########################
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
