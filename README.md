# ME405 Romi Robot Overview

**Project Name:** Romi Robot
**Brief Description:** This project involves assembling, programming, and testing a Romi robot for time-trial challenges. The goal is to navigate the printed game track fast and consistently.  
**Team Members:** Josh DeWeese and Jason Wong

![alt text](https://github.com/jwong32528/me405-romi-mecha21/blob/pictures/gametrack.png)
*Game Track*


## Introduction
The Romi Time-Trial project focuses on optimizing autonomous robot navigation using sensors and control algorithms. The primary objectives include:
- Developing a robust **line-following algorithm**.
- Ensuring **fast and consistent** lap times.
- Overcoming hardware and software challenges encountered during development.

## Mechanical and Electrical Design

### **Hardware Components:**
- **Motors:** Romi Motor 4.5 V
- **Sensors:** QTRX-HD-15A Reflectance Sensor Array, BNO055 IMU, Bump Sensors, Encoders
- **Microcontroller:** NUCLEO-L476RG (STM32L476RG MCU)
- **Power Supply:** 6 X AA Batteries

### **Wiring and Assembly:**
- Components are wired to ensure **minimum signal noise and interference**.
- **Wiring Diagram:**

### **Design:**
- Sensor placement optimization for **improved track detection**.
- Custom **mounting brackets** for sensor stability.


## 4. Software and Control Implementation
### **Programming Language and Libraries:**
- Python 3.9

### **Classes:**
**Main**
- motor
- encoder
- controls
- linesensor
- bumpsensor
- button handler
- imu
**Utility**
- cotask
- taskshare
- cqueue
- linesensor calibration
- imu calibration
- utils

### **Control System Overview:**
The robot implements a **PID control controller** to adjust motor speeds based on sensor feedback. 
- **Receives data from the line sensor and normalizes the data to output a centroid**
- **Romi uses the centroid to trace the lines on the game track**
- **Stable tracking**
- **Consistent Line Tracing**

### **State Machine / Task Flow:**
- **Idle:** Robot waits for button press
- **Line Following:** PID controller for tracing the lines.
- **Pivot Mode:** Uses IMU to measure initial heading as reference for rotating Romi based on a fixed angle displacement.
- **Straight Mode:** The robot moves forward.



## Challenges

## Results

## How to Reproduce Project

## Future Improvements

## Conclusion




**Video:** 





