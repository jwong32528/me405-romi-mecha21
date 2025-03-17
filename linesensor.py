# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 11:03:59 2025

@author: joshd
"""

from pyb import ADC, Pin

# This is linesensor.py
class LineSensor:

    
    def __init__(self, mode_share):
        
        self.mode_share = mode_share
        self.last_normalized_values = [0] * 8

        # Initializes each sensor by assigning correct pins
        self.sensors = {
            "s1": ADC(Pin("A4")),
            "s3": ADC(Pin("B0")),
            "s5": ADC(Pin("C2")),
            "s7": ADC(Pin("C3")),
            "s9": ADC(Pin("C5")),
            "s11": ADC(Pin("B1")),
            "s13": ADC(Pin("C4")),
            "s15": ADC(Pin("C1"))
        }
       
        # we were unable to calibrate in real time
        # Stored manually collected data as a tuple
        self.calibration_data = [
        #    MIN    MAX
            (304, 2624), 
            (264, 2246), 
            (261, 2447), 
            (256, 2111), 
            (254, 2217), 
            (265, 2354), 
            (256, 2340), 
            (305, 2619)
        ]
        
        
        
        # Define sensor weights for centroid calculation
        self.weights = [1, 2, 3, 4, 5, 6, 7, 8]  # 8 sensor setup with symmetrical weights


    def read_sensors(self):
        """Reads only the odd-numbered sensor values and returns them as a list."""
        return [self.sensors[key].read() for key in ["s1", "s3", "s5", "s7", "s9", "s11", "s13", "s15"]]

        
    def calibrate_sensors(self):
        """Calibrates sensors by measuring values on black and white surfaces."""
        input("Place the sensor array on a black surface and press Enter to continue...")
        black_readings = self.read_sensors()
        
        input("Place the sensor array on a white surface and press Enter to continue...")
        white_readings = self.read_sensors()

        # Ensure min is always the lower value
        self.calibration_data = tuple(
            (min(b, w), max(b, w)) for b, w in zip(black_readings, white_readings)
        )

        print(f"\nCalibration complete: {self.calibration_data}")  # Debugging
        

    def get_centroid(self):
        """Computes the centroid of the detected line based on weighted sensor values."""
        if self.calibration_data is None:
            print("Error: Calibration data is missing! Run calibrate_sensors() first.")
            return 0  

        # Define sensor positions (weights) from leftmost (-4) to rightmost (4)
        weights = [1, 2, 3, 4, 5, 6, 7, 8]
    
        sensor_keys = ["s1", "s3", "s5", "s7", "s9", "s11", "s13", "s15"]
        normalized_values = []
    
        # Normalize sensor readings based on calibration
        for i, key in enumerate(sensor_keys):  
            min_val, max_val = self.calibration_data[i]
            raw_value = self.sensors[key].read()
        
            # Normalize with clamping
            if max_val != min_val:
                norm_value = (raw_value - min_val) / (max_val - min_val)
                norm_value = max(0, min(1, norm_value))  # Ensure within [0,1]
                
                # This if statement uses the normalized value to declare if the sensor reads black or white
                if(norm_value >= 0.5):
                    norm_value = 1
                else:
                    norm_value = 0  
                    
            else:
                norm_value = 0  
                
            
            # Now we have a matrix where each sensor shows 0 for white and 1 for black
            normalized_values.append(norm_value)
            
        # Store the latest normalizes line sensor readings
        self.last_normalized_values = normalized_values

        # Now each sensor is multiplied by the weight to get values when they are black (1) and zeros when they are white (0)
        weighted_sum = sum(n * w for n, w in zip(normalized_values, weights))
        
        # These weighted are added together
        normalized_sum = sum(normalized_values)
        
        # This is divided by the normalized sum
        if normalized_sum == 0:
            centroid = 4.5
        else:
            centroid = weighted_sum / normalized_sum
        
        # Debugging output **to mimic plot structure**
        #print("\nSensor Values (0 = White, 1 = Black):")
        for w, v in zip(weights, normalized_values):
            print(f"Sensor {w}: {v:.3f}")

        print(f"\nCentroid: {centroid:.2f}")
        
        
        return centroid
    
    def get_normalized_values(self):

        return self.last_normalized_values
    