# -*- coding: utf-8 -*-
"""
Created on Mon Mar 10 11:21:54 2025

@author: joshd
"""

# utils.py
def normalize_error(error):
    """ Normalize angle error to be within -180 to 180 degrees. """
    while error > 180:
        error -= 360
    while error < -180:
        error += 360
    return error
