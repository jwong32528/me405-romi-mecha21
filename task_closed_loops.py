# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 11:12:14 2025

@author: joshd
"""

# !!! Potentially use this as a task running in the scheduler
# **Task functions for cooperative multitasking (`cotask`)**
def task_closed_loop_left(shares):
    """Task to maintain left motor speed."""
    controls, left_effort_share, left_velocity_share, left_dt_share, left_position_share = shares  # Get Controls object
    
    while True:
        controls.closed_loop_left(left_effort_share, left_velocity_share, left_dt_share, left_position_share)
        yield  # Yield control to scheduler

def task_closed_loop_right(shares):
    """Task to maintain right motor speed."""
    controls, right_effort_share, right_velocity_share, right_dt_share, right_position_share = shares  # Get Controls object
    
    while True:
        controls.closed_loop_right(right_effort_share, right_velocity_share, right_dt_share, right_position_share)
        yield  # Yield control to scheduler
   