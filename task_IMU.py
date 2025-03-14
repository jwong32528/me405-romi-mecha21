# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 10:58:32 2025

@author: joshd
"""

from utils import normalize_error

#!!! Eventually move this to a separate file
def task_imu(shares):
    imu, heading_share, datum_share, mode_share = shares
    
    #Task to read the IMU heading, detect 90-degree turns, and change mode.
    # Get initial heading as the datum
    euler_angles = imu.euler()
    if euler_angles is None:
        print("[ERROR] IMU not responding!")
        return
    
    datum_heading = euler_angles[0]  # ✅ Store initial heading
    datum_share.put(datum_heading)
    
    print(f"[DEBUG] Initial Datum Heading: {datum_heading:.2f}°")

    #diamond_check = False

    while True:
        # Get updated heading
        euler_angles = imu.euler()
        if euler_angles is None:
            print("[ERROR] IMU not responding!")
            yield
            continue

        current_heading = euler_angles[0]  # ✅ Continuously updating
        heading_share.put(current_heading)

        # Compute relative heading change
        heading_change = normalize_error(current_heading - datum_heading)

        # Debug: Show heading change
        print(f"[DEBUG] Datum: {datum_heading:.2f}°, Current Heading: {current_heading:.2f}°, Change: {heading_change:.2f}°")

        
        ## Detect 90-degree turn
        #if not diamond_check and abs(heading_change) >= 93:
        #    mode_share.put(1)  # ✅ Change mode to 1 after turning 90°
        #    diamond_check = True
        #    print("[DEBUG] 90-degree turn detected! Mode changed to 1")

        #if diamond_check == True:
        #    print("[DEBUG] 90-degree turn detected! Mode changed to 1")
        
        
        yield  # Allow other tasks to run
        