import time
from utils import normalize_error

  

class Controls:
    def __init__(self, Kp, Ki, Kd, V_ref_r, V_ref_l, Kp_2, Ki_2, Kd_2, Kp_3, 
                 Ki_3, Kd_3, pivot_max_effort, left_base_effort, 
                 right_base_effort, sensor, battery_voltage_share, 
                 left_encoder, right_encoder, left_motor, right_motor, 
                 centroid_share):
        
        # Get battery voltage from main()
        self.battery_voltage = float(battery_voltage_share.get())
        print(f"Using battery voltage: {self.battery_voltage}")
        
        self.left_encoder = left_encoder
        self.right_encoder = right_encoder
        self.left_motor = left_motor
        self.right_motor = right_motor
        
        # Uses the battery voltage to adjust the base effort because using 
        #  closed loop is very buggy
        C = 0.7  # Empirical correction factor
        voltage_factor_effort = 1 + C * (9.0 / self.battery_voltage - 1)
        self.base_effort = 15 * voltage_factor_effort
        
        voltage_factor = 9.0 / self.battery_voltage
        
        self.Kp = Kp * voltage_factor
        self.Ki = Ki * voltage_factor
        self.Kd = Kd * voltage_factor
        self.Kp_2 = Kp_2 * voltage_factor
        self.Ki_2 = Ki_2 * voltage_factor
        self.Kd_2 = Kd_2 * voltage_factor
        self.Kp_3 = Kp_3 * voltage_factor
        self.Ki_3 = Ki_3 * voltage_factor
        self.Kd_3 = Kd_3 * voltage_factor
        
        self.pivot_max_effort = pivot_max_effort
        
        self.left_base_effort = left_base_effort
        self.right_base_effort = right_base_effort
        
        self.V_ref_r = V_ref_r
        self.V_ref_l = V_ref_l
        self.integral = 0
        self.prev_error = 0
        self.prev_time = time.time()
    
        self.sensor = sensor 
        self.centroid_share = centroid_share
        
        # ✅ Store motor efforts
        self.left_effort = 0
        self.right_effort = 0
        
    
    def adjust_speed(self, left_effort_share, right_effort_share, left_dt_share):
        #Adjusts Romi's motor speed based on centroid data from the LineSensor.
        #centroid = sensor.get_centroid()  # Get centroid value
        centroid = self.centroid_share.get()

        # ✅ Normalize centroid from [-4, 4] to [-1, 1]
        #max_centroid = 4
        error = centroid - 4.5 #/ max_centroid  
        
        #current_time = time.time() # I dont think this is needed if we use encoder dt
        dt = left_dt_share.get()#self.left_encoder.dt #current_time - self.prev_time
        print(f"adjust speed dt: {dt}")

        #err = centroid  # Centroid is already in range -1 to 1
        P = self.Kp * error
        self.integral += error * dt
        I = self.Ki * self.integral
        D = self.Kd * ((error - self.prev_error) / dt if dt > 0 else 0)

        output = max(-100, min(100, (P + I + D))) #* abs(centroid)))  # Clamp output between -100 and 100

        print(f"P: {P}, I: {I}, D: {D} Output:{output} centroid: {centroid} ")
        
        
        # Apply correction to motors if centroid deviates at least 0.1
        # Since adjust speed is overriding the effort inputs form the left and
        # right closed loop tasks, this means this task is independent and the
        # output is currently relying purly on error to follow the line. 
        # Instead, we need to add and subtract output from the desired velocity
        # That the closed loop tasks are using. So maybe, the closed loop tasks
        # run first and add that output to a share, and then since the adjust
        # speed is moving afterwards, it can use those updates effort values 
        # to add adjustments to.
        
        # ✅ Read shared effort values
    
        #left_base_effort = self.base_effort #float(left_effort_share.get()) #20
        #right_base_effort = self.base_effort #float(right_effort_share.get()) #20
        
        #print(f"Base Efforts: Left={left_base_effort}, Right={right_base_effort}")
        print(f"Correction: {output}")
        
        
        if centroid > 4.5:
            final_left_effort = self.left_base_effort + output
            final_right_effort = max(0, self.right_base_effort - output)
            print("centroid > 0.75")
            print(f"Final Efforts: Left={final_left_effort}, Right={final_right_effort}")
            
            self.left_motor.set_effort(final_left_effort)
            self.right_motor.set_effort(final_right_effort)
            
            
        elif centroid < 4.5:
            final_left_effort = max(0, self.left_base_effort + output) # in this state i think the output is negative?
            final_right_effort = self.right_base_effort - output
            print("centroid < 0.75")
            print(f"Final Efforts: Left={final_left_effort}, Right={final_right_effort}")
            
            self.left_motor.set_effort(final_left_effort)
            self.right_motor.set_effort(final_right_effort)
            
            
        else:
            self.left_motor.set_effort(self.left_base_effort)
            self.right_motor.set_effort(self.right_base_effort)
        
        
        #left_motor.set_effort(left_base_effort)
        #right_motor.set_effort(right_base_effort)
            
        #If the centroid is between 0.05 and -0.05, the left and right closed
        # loop will take over because if all three are running at the same 
        # period, adjust speed is added to the scheduler last and overrides
        # the effort value (pseudo higher priority)
        
        #left_motor.set_effort(output if centroid > 0.03 else -output)
        #right_motor.set_effort(-output if centroid > 0.03 else output)

        self.prev_error = error
        #self.prev_time = current_time
    
    

    # !!! Col said kd is what is causing the choppyness, consider not using
    def closed_loop_left(self, left_effort_share, left_velocity_share, left_dt_share, left_position_share):
        """Keeps the left motor running at a constant speed while allowing adjustments."""
    #!!! Add Jason's changes HOWEVER
    #!!! USE THE SHARES I MADE THAT THE ENCODER TASK UPDATES INSTEAD OF RECREATING dt!
    #!!! We can also make a PID class that closed_loop, adjust_speed, adjust_heading references
    
        #current_time = time.time()           # Gets current Time
        #dt = current_time - self.prev_time   # Gets change in time
        dt = left_dt_share.get()#self.left_encoder.dt
        #self.left_encoder.update()                # Turn new encoder reading to current
        V_meas = left_velocity_share.get() #self.left_encoder.get_velocity() # Gets the velocity of the encoder
        
        print(f"Reference Velocity: {self.V_ref_l}")
        print(f"L: {V_meas}")
        error = self.V_ref_l - V_meas          # Subtracts from the 
        print(f"err: {error}")

        print(f"dt: {dt}")  # Check dt values

        P = self.Kp_2 * error
        self.integral += error * dt
        I = self.Ki_2 * self.integral
        D = self.Kd_2 * ((error - self.prev_error) / dt if dt > 0 else 0)

        # ✅ Debug Print: Check error changes, dt, and D calculation
        print(f"Dt: {dt}, Err: {error}, Prev Err: {self.prev_error}, Err Diff: {error - self.prev_error}, D: {D}")

        PID = P + I + D        
        
        self.left_effort = max(-100, min(100, P + I + D))  
        
        print(f"LEFT_CLOSED_LOOP - P: {P}, I: {I}, D: {D}, Output: {PID}")

        # Debugging: Check when the failsafe is triggered
        if abs(V_meas) > (self.V_ref_l * 1.5):
            print("Warning: Left motor is spinning too fast! Limiting effort.")

        #left_motor.set_effort(self.left_effort)  
        left_effort_share.put(float(self.left_effort))  # ✅ Store effort in shared variable

        self.prev_error = error
        #self.prev_time = current_time


    def closed_loop_right(self, right_effort_share, right_velocity_share, right_dt_share, right_position_share):
        """Keeps the right motor running at a constant speed while allowing adjustments."""
    
    #!!! Add Jason's changes HOWEVER
    #!!! USE THE SHARES I MADE THAT THE ENCODER TASK UPDATES INSTEAD OF RECREATING dt!
    #!!! We can also make a PID class that closed_loop, adjust_speed, adjust_heading references
    
        #current_time = time.time()
        #dt = current_time - self.prev_time
        dt = right_dt_share.get() #self.right_encoder.dt
        self.right_encoder.update()
        V_meas = right_velocity_share.get() #self.right_encoder.get_velocity()
        
        print(f"R {V_meas}")
        error = self.V_ref_r - V_meas

        P = self.Kp_2 * error
        self.integral += error * dt
        I = self.Ki_2 * self.integral
        D = self.Kd_2 * ((error - self.prev_error) / dt if dt > 0 else 0)

        PID = P + I + D

        self.right_effort = max(-100, min(100, PID))  

        print(f"RIGHT_CLOSED_LOOP - P: {P}, I: {I}, D: {D}, Output: {PID}")        

        # Debugging: Check when the failsafe is triggered
        if abs(V_meas) > (self.V_ref_r * 1.5):
            print("Warning: Right motor is spinning too fast! Limiting effort.")

        #right_motor.set_effort(self.right_effort)  
        right_effort_share.put(float(self.right_effort))  # ✅ Store effort in shared variable

        self.prev_error = error
        #self.prev_time = current_time

    def basic_go_straight(self, left_effort_share, right_effort_share):
       
    # !!! WE SHOUD DEFINITLY REPLACE THIS BECASUE ROMI DOES NOT MOVE STRAIGHT    
    
        # ✅ Read shared effort values
        #left_base_effort = 15#float(left_effort_share.get()) #self.base_effort#
        #right_base_effort = 14.7#float(right_effort_share.get()) #self.base_effort#
        
        print("left_base_effort")
        
        self.left_motor.set_effort(self.left_base_effort)
        self.right_motor.set_effort(self.right_base_effort)
        
    def idle(self):
       
    # !!! WE SHOUD DEFINITLY REPLACE THIS BECASUE ROMI DOES NOT MOVE STRAIGHT    
    
        # ✅ Read shared effort values
        #left_base_effort = 15#float(left_effort_share.get()) #self.base_effort#
        #right_base_effort = 14.7#float(right_effort_share.get()) #self.base_effort#
        
        print("left_base_effort")
        
        self.left_motor.set_effort(0)
        self.right_motor.set_effort(0)

    def adjust_heading(self, desired_heading, heading_share, mode_share, left_dt_share):
        
        # Get current heading from the shared variable (updated by task_imu)
        current_heading = heading_share.get()

        # Calculate error and normalize it
        error = normalize_error(desired_heading - current_heading)

        
        dt = left_dt_share.get()#self.left_encoder.dt #current_time - self.prev_time
        print(f"adjust speed dt: {dt}")

        #err = centroid  # Centroid is already in range -1 to 1
        P = self.Kp_3 * error
        self.integral += error * dt
        I = self.Ki_3 * self.integral
        D = self.Kd_3 * ((error - self.prev_error) / dt if dt > 0 else 0)

        output = max(-self.pivot_max_effort, min(self.pivot_max_effort, (P + I + D))) #* abs(centroid)))  # Clamp output between -100 and 100


        # Debugging
        print(f"[DEBUG] Desired: {desired_heading:.2f}°, Current: {current_heading:.2f}°, Error: {error:.2f}°, Effort: {output:.2f}")

        # Stop motors when the heading is reached
        if abs(error) < 1:
            self.left_motor.set_effort(0)
            self.right_motor.set_effort(0)
            print("[DEBUG] Target heading reached, stopping motors.")
            
        # ✅ Handle 180° case to avoid oscillation
        if abs(error) == 180:
            output = self.pivot_max_effort if desired_heading > current_heading else -self.pivot_max_effort
            print("[DEBUG] 180-degree case detected. Forcing initial turn direction.")
        
        # Apply motor efforts for pivoting
        self.left_motor.set_effort(output)
        self.right_motor.set_effort(-output)
        
        """
        # ✅ Settling time check (only switch states if stable for 5 cycles)
        if abs(error) < 6:  # Within tolerance
            self.settling_counter += 1  # Count stable cycles
            if self.settling_counter >= 5:  # ✅ Prevents instant state change
                self.left_motor.set_effort(0)
                self.right_motor.set_effort(0)
                mode_share.put(2)  # ✅ Change to state 2 after being stable
                print("[DEBUG] Target heading reached. Changing state!")
                mode_share.get()
        else:
            self.settling_counter = 0  # Reset if Romi is not stable
        """
        
        self.prev_error = error
  