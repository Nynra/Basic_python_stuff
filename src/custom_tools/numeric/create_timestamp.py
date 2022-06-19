# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 22:35:14 2022.

@author: Nynra
"""


def create_timestamp(n, samplerate):
    """Return a timestamp column."""
    return [i * 1 / samplerate for i in range(n)]
