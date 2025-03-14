# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 10:59:26 2025

@author: joshd
"""

      
# !!! Eventually move this to a separate file
def task_encoder(shares):
    
    left_encoder, right_encoder, left_position_share, right_position_share, left_velocity_share, right_velocity_share, left_dt_share, right_dt_share, grid_share, mode_share = shares
    
    #diamond_position_on = 5 * 1440
    #diamond_position_off = 6 * 1440
    
    past_dashed_lines = 17.5 * 1440
    
    #mode_activated = False
    
    #past_dashed_line = 12 * 1440
    
    # Task to update encoder readings and store position & velocity in shared variables. 
    while True:
        left_encoder.update()
        right_encoder.update()
        
        left_position_share.put(left_encoder.get_position())
        right_position_share.put(right_encoder.get_position())
        
        left_velocity_share.put(left_encoder.get_velocity())
        LV = left_velocity_share.get()
        print(f"Encoder LV: {LV}")
        right_velocity_share.put(right_encoder.get_velocity())
        RV = right_velocity_share.get()
        print(f"Encoder RV: {RV}")
        
        
        # ✅ Store dt values from encoders into shared variables
        #before = left_dt_share.get()
        #print(f"encoder task dt before: {before}")
        
        left_dt_share.put(left_encoder.dt)
        
        #after = left_dt_share.get()
        #print(f"encoder task dt after: {after}")
        
        right_dt_share.put(right_encoder.dt)
        
        #!!! Seems to cause linesensor to stop working
        # Allows Line Sensor to start searching for the grid
        if left_position_share.get() >= past_dashed_lines:
            grid_share.put(1)
    
        
        ## !!! THERE IS A BUG WHERE ROMI STAYS IN STATE 4 IF THIS IF STATEMENT IS ACTIVATED BEFORE ROMI HITS THE 90 DEGREE ANGLE
        ## ✅ Check if left encoder has reached 6 full rotations (Disable Mode)
        #if not mode_activated and abs(left_encoder.position) >= diamond_position_off:
        #    mode_share.put(1)  # ✅ Turn off STRAIGHT MODE
        #    print("🔄 Mode returned to LINE FOLLOW MODE (0) after 6 rotations")
        #    mode_activated = True  # ✅ Reset activation flag
        #    
        #if mode_activated == True:
        #    print("🔄 Mode returned to LINE FOLLOW MODE (0) after 6 rotations")
        
        
        
        
        yield  # Allow other tasks to run
        