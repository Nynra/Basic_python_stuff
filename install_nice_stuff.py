# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 20:06:44 2021.

@author: baskl
"""
import os
import subprocess
import sys


def install_package(package_name):
    # Install most recent version
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])


supported_systems = ['Debian Buster', 'Ubuntu']
os_name = os.system()
