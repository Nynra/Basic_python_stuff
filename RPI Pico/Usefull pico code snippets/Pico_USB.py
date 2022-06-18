# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 21:50:32 2021.

@author: baskl
"""
import select
import sys


class USB_comm():
    """A class to manage the communication with the main computer."""

    def __init__(self):
        """
        Initialize the communication.

        Returns
        -------
        None.

        """
        # Create the buffer polling object and set to check incoming data
        self.poll = select.poll()
        self.poll.register(sys.stdin, select.POLLIN)

    def write(self, ccode, attr=[]):
        """Parse the command and attributes and send to main computer."""
        msg = ccode
        for i in attr:
            msg += i + ':'  # Append all the attributes
        msg += ';\n'  # Close the message
        print(msg)

    def read(self, timeout=20):
        """
        Read and parse the command and attributes.

        Returns
        -------
        string
            The id code of the command.
        [string, ...]
            List containing the attributes of the command.

        """
        # Read the buffer
        msg = ''
        while True:
            res = self.poll.poll(10)  # Poll with 10ms timeout
            if len(res) > 0:    # Check if there is a message
                ch = res[0][0].read(1)
                msg += ch
                if ch == ';':  # Xommand is complete
                    break
            else:
                # There is no waiting command
                return None, None

        # Remove the last character and split on ':'
        attr = msg[:-1].split(':')  # Get the attributes
        ccode = attr.pop(0)  # Get the command code
        return ccode, attr

    def handshake(self, timeout=300):
        """Perform handhake with the main computer."""
        while True:  # Wait for the message
            res, _ = self.read()
            if res == 'Hello there.':
                break

        self.write('Hello there General Kenobi.')
