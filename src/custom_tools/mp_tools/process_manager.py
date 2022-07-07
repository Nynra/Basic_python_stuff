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

    def wait(self):
        """Wait for all the threads to finish."""
        for t in self._threads:
            t.join()


if __name__ == '__main__':
    def good_worker():
        print("GoodWorker Starting")
        time.sleep(4)

    def bad_worker():
        print("[BadWorker] Starting")
        time.sleep(2)
        raise Exception("ups!")

    # Create the manager
    proc_manager = Process_manager()

    # Add some workers
    proc_manager.launch_proc(good_worker)
    # proc_manager.launch_proc(good_worker)
    # proc_manager.launch_proc(bad_worker)

    # Wait for all the workers to finish
    proc_manager.wait()

    # Check if there were errors
    if proc_manager.errors_flag:
        print("Errors flag is set: some process crashed")
    else:
        print("Everything closed cleanly")
