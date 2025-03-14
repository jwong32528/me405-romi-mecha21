from pyb import Pin
import utime

# Initialize bump sensor pins
bump_pins = [
    Pin("C9", Pin.IN, Pin.PULL_UP),
    Pin("C8", Pin.IN, Pin.PULL_UP),
    Pin("C6", Pin.IN, Pin.PULL_UP),
    Pin("C10", Pin.IN, Pin.PULL_UP),
    Pin("C12", Pin.IN, Pin.PULL_UP),
    Pin("A15", Pin.IN, Pin.PULL_UP)
]

# Dictionary to store last press times for multiple bump sensors
last_bump_times = {}

def bump_detected(debounce_time=50):
    """Checks if any bump sensor is pressed and applies debouncing.
    
    Args:
        debounce_time (int): Time in milliseconds to prevent bouncing.
    
    Returns:
        int: The index of the pressed bump sensor (0 to 5), or -1 if none are pressed.
    """
    global last_bump_times
    current_time = utime.ticks_ms()

    for i, bump_pin in enumerate(bump_pins):
        pin_name = bump_pin.name()  # Get unique pin identifier

        # Initialize last_bump_times entry if it doesn't exist
        if pin_name not in last_bump_times:
            last_bump_times[pin_name] = 0

        # Check if button is pressed and debounce
        if bump_pin.value() == 0 and (utime.ticks_diff(current_time, last_bump_times[pin_name]) > debounce_time):
            last_bump_times[pin_name] = current_time
            return i  # Return the index of the pressed bump sensor

    return -1  # No bump detected

    

    

    
    
    


