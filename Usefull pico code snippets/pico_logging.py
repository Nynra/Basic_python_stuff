# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 23:15:53 2021.

@author: baskl
"""
import os

class Logger():
    """Class to emulate a simple logger."""

    def __init__(self, log_lvl, filename='log.log'):
        """Initialize the logging object."""
        # Set up the priority dict adn set entry nr to 0
        self.log_entry = 0
        self.priority = {'debug': 5,
                         'info': 4,
                         'warning': 3,
                         'error': 2,
                         'critical': 1}
        
        # Set the logging priority and open logging file
        self.logging_lvl = self.priority[log_lvl.lower()]
        try:
            # Check if there already is a logfile
            self.log_file = open(filename, 'r+')
        except OSError:  # Create a new log file
            self.log_file = open(filename, 'w')
            
        self.am_logging = True

    def log(self, lvl, msg):
        """Log a message."""
        if lvl.lower() in self.priority.keys() and \
                self.priority[lvl.lower()] >= self.logging_lvl:
            # Log the msg if the lvl corresponds
            self.log_file.write('{} : {} : {}\n'.format(self.log_entry, lvl,
                                                      msg))
            self.log_file.flush()
            self.log_entry += 1
            
    def debug(self, msg):
        """Log on debug level."""
        self.log('debug', msg)
        
    def info(self, msg):
        """Log on info level."""
        self.log('info', msg)
        
    def warning(self, msg):
        """Log on warning level."""
        self.log('warning', msg)
        
    def error(self, msg):
        """Log on error level."""
        self.log('error')
        
    def critical(self, msg):
        """Log on critical level."""
        self.log('critical', msg)

    def start_logging(self, log_lvl, filename='log.log'):
        """Start logging."""
        if self.am_logging:
            self.critical('You cant start a new log when a log is already open.')
            return
        self.__init__(log_lvl=log_lvl, filename=filename)
        
    def quit_logging(self):
        """Quit logging and save the file."""
        self.log_file.close()
        self.am_logging = False

