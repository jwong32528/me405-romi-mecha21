# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 11:10:49 2025

@author: joshd
"""

from utils import normalize_error
import cqueue
import bump


def task_controls(shares):
  
    
    
    #print(f"DEBUG: shares received in task_controls: {shares}")  # Debug print
    #The task where the finite state diagram will be within. 
    #In the controls task, there are different modes 
    #that are listed above. A share is used to determine which state/mode romi 
    #is in.

    #Line sensor will send shares based on the senso readings
    #Then the controls task can utilize the line sensor centroid and the IMU euler
    #data to switch between. Basically the controls task IS the supervisor.
    
    
    controls, left_effort_share, right_effort_share, left_dt_share, right_dt_share, left_position_share, right_position_share, left_velocity_share, right_velocity_share, heading_share, datum_share, mode_share = shares  # Get Controls object
    
    S0_LINE_FOLLOW_MODE     = 0
    S1_PIVOT_MODE           = 1
    S2_STRAIGHT_DIST_MODE   = 2
    S3_WALL_BUMP_MODE       = 3 # Not Needed
    S4_DIAMOND_MODE         = 4 # Not Needed
    S5_FINISH_LINE_MODE     = 5
    
    #straight_start_pos = None  # Track starting encoder position
    #straight_distance_threshold = 100  # Target encoder ticks to switch back
    
    #desired_heading = 90 # Replace this with heading queue
    heading_queue = cqueue.FloatQueue(10) # degress from the starting datum
    
    #target_displacement = 1440 * 2
    distance_queue = cqueue.FloatQueue(10) # Number of wheel rotations
    
    # updates mode_share
    supervisor_queue = cqueue.FloatQueue(10)
    
    
    # Diamond
    heading_queue.put(86)
    distance_queue.put(0.05 * 1440)
    supervisor_queue.put(0)
    
    # Grid
    heading_queue.put(180)
    distance_queue.put(3 * 1440)
    supervisor_queue.put(1)
    
    heading_queue.put(270)
    distance_queue.put(3 * 1440)
    supervisor_queue.put(1)
    
    # Wall
    heading_queue.put(0)
    distance_queue.put(1.3 * 1440)
    supervisor_queue.put(1)
    
    heading_queue.put(270)
    distance_queue.put(0.8 * 1440)
    supervisor_queue.put(1)
    
    heading_queue.put(180)
    distance_queue.put(0.05 * 1440)
    supervisor_queue.put(0)
        
    current_heading_target = None  # Store current heading until reached
    current_displacement_target = None  # Store current displacement until reached
    initial_position = None  # Track where Romi started moving

    
   
    
    while True:
        try:
            
            current_mode = mode_share.get()
            print(f"Current Mode: {current_mode}")
            
            state = mode_share.get()
            # State 0 - Initialization
            if (state == S0_LINE_FOLLOW_MODE):
                # This mode will move forward while adjusting for a line
                #controls.closed_loop_left(left_effort_share, left_velocity_share, left_dt_share)
                #controls.closed_loop_right(right_effort_share, right_velocity_share, right_dt_share)
                
        
                bump_index = bump.bump_detected()
                if bump_index != -1:
                    print(f"[ALERT] Bump detected on sensor {bump_index + 1}! Switching to PIVOT mode.")
                    mode_share.put(S5_FINISH_LINE_MODE)  # Force idle mode immediately
                    yield  # Wait for the next scheduler cycle
                
                
                print("Line Follow Mode")
                controls.adjust_speed(left_effort_share, right_effort_share, left_dt_share)
                
                yield
                
                
            elif (state == S1_PIVOT_MODE): 
                
                
                if current_heading_target is None and heading_queue.any():  
                    # Get a new heading when the mode first switches
                    heading_displacement = heading_queue.get()
                    
                    current_heading_target = datum_share.get() + heading_displacement
                    
                    print(f"[DEBUG] Pivoting to {current_heading_target}°")

                if current_heading_target is not None:
                    controls.adjust_heading(current_heading_target, heading_share, mode_share, left_dt_share)

                    # When the heading is reached, switch to straight mode
                    if abs(normalize_error(current_heading_target - heading_share.get())) < 2:
                        print("[DEBUG] Heading reached! Switching to STRAIGHT mode.")
                        current_heading_target = None  # Reset for next switch
                        mode_share.put(S2_STRAIGHT_DIST_MODE)
               
                
                # adjust heading will switch to state 2 when finished with heading
                
                
                #controls.adjust_heading(desired_heading, heading_share, mode_share)
                
                yield

                
            elif (state == S2_STRAIGHT_DIST_MODE):
                
                if current_displacement_target is None and distance_queue.any():
                    # Get a new distance when the mode first switches
                    current_displacement_target = distance_queue.get()
                    initial_position = left_position_share.get()  # Store starting position
                    print(f"[DEBUG] Moving forward {current_displacement_target} encoder ticks")

                print(f"Current_Displacement_Target: {current_displacement_target}")
                print(f"Initial Position: {initial_position}")

                if current_displacement_target is not None:
                    
                    
                    
                    # Check if bump sensor was triggered **before** displacement check
                    bump_index = bump.bump_detected()
                    if bump_index != -1:
                        print(f"[ALERT] Bump detected on sensor {bump_index + 1}! Stopping early.")
                        current_displacement_target = None  # Reset target distance
                        
                        supervisor = supervisor_queue.get()
                        mode_share.put(supervisor)
                        #mode_share.put(S1_PIVOT_MODE)  # Change to pivot mode immediately
                        
                        yield  # Stop here until next scheduler cycle
                    
                    
                    
                    # Check if we've reached the target displacement
                    current_position = left_position_share.get()
                    print(f"Curent Position: {current_position}")
                    
                    if abs(current_position - initial_position) >= current_displacement_target:
                        print("[DEBUG] Target distance reached! Switching to PIVOT mode.")
                        current_displacement_target = None  # Reset for next switch
                        
                        #mode_share.put(S1_PIVOT_MODE)
                        
                        #!!! once supervisor_queue added, replace line above with the line below
                        
                        supervisor = supervisor_queue.get()
                        mode_share.put(supervisor)
                          
                    controls.basic_go_straight(left_effort_share, right_effort_share)
                    
                
                yield
            
            
            
            elif (state == S3_WALL_BUMP_MODE):
                
                # UNUSED CODE
                controls.closed_loop_right(right_effort_share)
                yield
                
            
            
            elif (state == S4_DIAMOND_MODE):
                
                # Goes straight until encoder task changes back to state 0
                controls.basic_go_straight(left_effort_share, right_effort_share)
                yield
            
            
            elif (state == S5_FINISH_LINE_MODE):
                
                
                controls.idle()
                
                yield
                # Romi idles
                
        except Exception as e:
            print(f"Error in task_controls FSM: {e}")
            yield  # Ensure the task continues running even after an error        