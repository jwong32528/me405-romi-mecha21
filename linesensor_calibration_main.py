# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 11:00:51 2025

@author: joshd
"""



from task_linesensor import LineSensor  # Import the class from qtr_sensor.py

def main():
    #Main function to test the calibration process.
    qtr = LineSensor(None)  # Create an instance of the sensor array
    
    print("\nStarting calibration process...\n")
    calibration_result = qtr.calibrate_sensors()  # Run calibration
    
    print("\nFinal Calibration Data (Tuple Format):")
    print(calibration_result)  # Print calibration data for verification

# Run the test only if this file is executed directly
if __name__ == "__main__":
    main()

