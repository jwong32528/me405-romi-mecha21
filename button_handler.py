# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 13:06:35 2025

@author: joshd
"""

from pyb import Pin
import utime

# Setup GPIO pin for the Nucleo user button (PC13)
nucleo_button = Pin("PC13", Pin.IN, Pin.PULL_UP)

# Dictionary to store last press times for multiple buttons
last_press_times = {}

def button_pressed(button, debounce_time=50):
    """Non-blocking debounce function for any button press.
    
    Args:
        button (pyb.Pin): The button pin to check.
        debounce_time (int): Time in milliseconds to prevent bouncing.
    
    Returns:
        bool: True if the button press is valid, otherwise False.
    """
    global last_press_times

    pin_name = button.name()  # Get unique pin identifier
    current_time = utime.ticks_ms()

    # Initialize last_press_times entry if it doesn't exist
    if pin_name not in last_press_times:
        last_press_times[pin_name] = 0

    # Debounce check
    if button.value() == 0 and (utime.ticks_diff(current_time, last_press_times[pin_name]) > debounce_time):
        last_press_times[pin_name] = current_time
        return True
    return False
