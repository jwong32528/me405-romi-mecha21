def task_line_sensor(shares):
    """Task to continuously update centroid and mode_share."""
    sensor, centroid_share, grid_share, mode_share = shares  # Unpack shared variables

    # 
    diamond_flag = False
    grid_flag = False

    while True:
        centroid = sensor.get_centroid()  # Compute centroid
        # Store centroid in shared variable
        centroid_share.put(centroid)
        
        
        normalized_values = sensor.get_normalized_values()  # Get sensor readings
        

        active_sensors = sum(normalized_values)

        # Add flag to detect diamond once. And change to pivot state 
        if (active_sensors >= 3 and normalized_values[0] == 0 and normalized_values[7] == 0 and not diamond_flag):  
            if mode_share.get() == 0:  # Only update if mode was previously 0
                mode_share.put(1)  # Enter Pivot Mode
                diamond_flag = True
                print("Detected Diamond Switching to PIVOT MODE (1)")
        

        # Grid_share acts as a flag to start checking for  
        if grid_share.get() == 1: 
             if (normalized_values[1] == 0 and normalized_values[6] == 0 and all(normalized_values[i] == 0 for i in [2, 3, 4, 5]) and not grid_flag):  
                 if mode_share.get() == 0:  # Only update if mode was previously 0
                     mode_share.put(1)  # Enter Pivot Mode
                     grid_flag = True
                     #last_mode_change_time = current_time  # Reset the timer
                     print(" Mode updated to PIVOT MODE (1)")

        yield  # Yield for cooperative multitasking
