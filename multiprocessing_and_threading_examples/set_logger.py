# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 19:00:50 2022

@author: baskl
"""
import logging

# Set the logging level and format
FORMAT = '%(asctime)s %(levelname)s %(thread)d %(message)s'
log_file = 'logs\\node.log'

# Only warning and up are logged except when specificly set in the module
logger = logging.getLogger(__name__)
logging.basicConfig(filename=log_file, format=FORMAT,
                   level=logging.WARNING)
logger.critical('\n\n###### New Session Started ######\n')

# =============================================================================
# import logging
# 
# node = None
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# =============================================================================
