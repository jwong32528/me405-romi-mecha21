# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 11:01:47 2025

@author: joshd
"""
import time
from pyb import I2C
from BNO055 import BNO055

def main():
    # Initialize I2C and IMU
    i2c = I2C(1, I2C.MASTER, baudrate=400000)
    imu = BNO055(i2c)

    # Reset and set mode
    imu.set_mode(0x00)  # CONFIGMODE first
    time.sleep(0.1)
    imu.set_mode(0x0C)  # NDOF mode
    time.sleep(0.1)

    print("\n🚀 IMU Calibration Started. Follow these steps to calibrate:\n")
    print("1️⃣ Rotate the IMU **slowly in all directions** to calibrate the Gyro.")
    print("2️⃣ Hold the IMU **still in multiple positions** to calibrate the Accelerometer.")
    print("3️⃣ Move the IMU in a **figure-eight motion** to calibrate the Magnetometer.")
    print("🔄 Keep moving until all values reach 3.\n")

    while True:
        # Get calibration status
        status = imu.get_calibration_status()
        print(f"[DEBUG] Calibration Status: {status}")

        # If fully calibrated, save data and exit
        if all(value == 3 for value in status.values()):
            print("\n✅ IMU Fully Calibrated! Saving calibration data...\n")

            # Save calibration data
            calibration_data = imu.get_calibration_data()
            with open("imu_calibration.dat", "wb") as f:
                f.write(calibration_data)

            print("💾 Calibration data saved as 'imu_calibration.dat'.")
            print("🎯 You can now run your main program!")
            break

        time.sleep(1)  # Wait before checking again

if __name__ == "__main__":
    main()