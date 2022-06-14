# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 18:11:26 2022.

@author: baskl
"""
from multiprocessing import Event, Pipe, Process
from pipe_com import close_pipe, write_pipe, read_pipe, SENTINEL
from time import time, sleep
from threading import Thread


class Thread_format():
    """The basic form of a thread."""

    def start(self, pipe_con, shutdown_event):
        """Start the process."""
        self.shutdown_event = shutdown_event
        self.pipe_con = pipe_con
        self.thread = Thread(target=self.update, args=(pipe_con,
                                                       shutdown_event,))
        self.thread.start()

    def stop(self):
        """Stop the process."""
        self.shutdown_event.set()

    def update(self, pipe_con, shutdown_event):
        """Do the processing stuff."""
        while not shutdown_event.is_set():
            # Do something
            sleep(0.01)
            write_pipe(pipe_con, [1, 2, 3])

        # Send conformation to the other end of the pipe
        write_pipe(pipe_con, SENTINEL)

        # Clean up the mess the process made
        self.cleanup()

    def cleanup(self):
        """Clean up the mess before the process exits."""
        close_pipe(self.pipe_con)


class Process_format():
    """The basic form of a process/thread."""

    def start(self, pipe_con, shutdown_event):
        """Start the process."""
        self.shutdown_event = shutdown_event
        self.pipe_con = pipe_con
        self.process = Process(target=self.update, args=(pipe_con,
                                                         shutdown_event,))
        self.process.start()

    def stop(self):
        """Stop the process."""
        self.shutdown_event.set()

    def terminate(self):
        """Force the process to stop."""
        self.process.terminate()

    def update(self, pipe_con, shutdown_event):
        """Do the processing stuff."""
        while not shutdown_event.is_set():
            # Do something
            sleep(0.01)
            write_pipe(pipe_con, [1, 2, 3])

        # Send conformation to the other end of the pipe
        write_pipe(pipe_con, SENTINEL)

        # Clean up the mess the process made
        self.cleanup()

    def cleanup(self):
        """Clean up the mess before the process exits."""
        close_pipe(self.pipe_con)


if __name__ == '__main__':
    """Example code of Process_format, Threading format works the same."""
    # Create the needed stuff
    x = Process_format()
    me, you = Pipe()
    shutdown_event = Event()

    # Start the process
    x.start(you, shutdown_event)
    duration = 5
    end_time = time() + duration

    # Wait a while for the process to do stuff
    while end_time > time():
        sleep(1)
        # Read the stuff
        content = read_pipe(me)
        print(content)

    # Give the shutdown signal
    # shutdown_event.set()
    x.stop()

    # Wait to receive conformation
    while True:
        content = read_pipe(me)
        print(content)
        if SENTINEL in content:
            break

    print('Found SENTINEL command')
    close_pipe(me)
