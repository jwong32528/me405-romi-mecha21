# ME405 Romi Robot Overview

**Project Name:** Romi Robot
**Brief Description:** This project involves assembling, programming, and testing a Romi robot for time-trial challenges. The goal is to navigate the printed game track fast and consistently.  
**Team Members:** Josh DeWeese and Jason Wong

![alt text](https://github.com/jwong32528/me405-romi-mecha21/blob/pictures/gametrack.png)
*Game Track*

## Table of Contents
- [Introduction](#introduction)
- [Mechanical and Electrical Design](#mechanical-and-electrical-design)
  - [Design Overview](#design-overview)
  - [Hardware Components](#hardware-components)
  - [Wiring and Assembly](#wiring-and-assembly)
  - [Design](#design)
- [Software and Control Implementation](#software-and-control-implementation)
  - [Software Overview](#software-overview)
  - [Programming Language and Libraries](#programming-language-and-libraries)
  - [Classes](#classes)
  - [Control System Overview](#control-system-overview)
  - [State Machine / Task Flow](#state-machine--task-flow)
- [Challenges](#challenges)
- [Results](#results)



## Introduction
The Romi Time-Trial project focuses on completing the game track using controls using various sensors as feedback. The primary objectives include:
- Developing a robust **line-following algorithm**.
- Ensuring **fast and consistent** lap times.
- Overcoming hardware and software challenges encountered during development.

## Mechanical and Electrical Design

### Design Overview
For the mechanical components of our Romi, we used a line sensor, two bump sensors, and an IMU. The line sensor was securely mounted directly onto the Romi’s chassis, positioned as low as possible without touching the ground to minimize reading errors. The IMU was mounted underneath the front of the chassis, while the bump sensors were attached to the front of the Romi.

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

### Software Overview

The main.py file is responsible for initializing and managing the core components of the Romi. It initializes the IMU, encoders, motors, and line sensor, and all the shared variables for communication between tasks, including the controller gains. The program initializes the encoder, IMU, linesensor, and controls tasks, appending the tasks to the scheduler, and running them at a 10 ms interval. 

The controls task implements a finite state machine to change its state from line following, to pivot, straight distance, and finish line mode. The controls task is used to hard code the distance and angle displacement of the Romi so that it is able to complete the track.  For the encoder task, we did not convert the encoder ticks directly to position, so we ended up using the resoltuion of 1440 counts/rev to get the target distance or revolutions. The linesensor task gets the sensor readings and normalizes the data so that white = 0 and black = 1, returning the centroid for line tracing. The IMU task acquires the heading data, which allows us to know the orientation of Romi at all times but with some error.



### **Programming Language and Libraries:**
- Python 3.9

### **Classes:**
**Main**
- motor: Initializes the motors, allowing for easy enabling/disabling, effort adjustments, and direction changes
- encoder: Initializes the encoders, reads tick counts, and converts them into position and velocity measurements
- linesensor: Reads and normalizes sensor data, then returns the centroid for line tracing
- controls: Implements a basic PID controller for line tracing using centroid data
- bumpsensor: Detects a bump
- button handler: Uses the button on the romi to run the romi
- imu: Acquires heading data from the magnometer to know the orientation of the Romi

**Utility**
- cotask: Manages cooperative multitasking, allowing multiple tasks to run efficiently
- taskshare: Facilitates data sharing between tasks, ensuring smooth communication
- cqueue: Implements a queue structure for task scheduling and data handling
- linesensor calibration: Calibrates the linesensor for black and white surfaces
- imu calibration: Calibrates the IMU to correct for sensor drift and improve heading accuracy
- utils: Used functions to reduce the amount of code in a file

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
The most challenging part of the game track was navigating the diamond section. This sharp turns made it difficult for Romi to stay on the line without veering off. To overcome this challenge, we programmed Romi to go straight through the diamond when the Romi detected the diamond. 
Another challenge was integrating both the PID controllers for line tracing and straight-line movement. Running both controllers simulatenously caused the velocity PID controller to adjust the velocity, even when we needed different velocities for turning. Due to time constraints and the fact that it was not essential, we decided not to incorporate the velocity controller. However, with more time, we would have implemented it specifically for the grid section to prevent the Romi from deviating from its straight path.
If we were to redo this project, we would eliminate the use of the line sensor and instead hard-code the Romi’s movement using predefined distances and angles. We found that the line sensor becomes unreliable at higher speeds, and we could achieve the same level of consistency without it.

## Results
We were able to successfully complete the game track in 48 seconds during the live demo. 

**Video:** 
[![Watch the Video](https://img.youtube.com/vi/Uyyd9d3AcY4/0.jpg)](https://youtu.be/Uyyd9d3AcY4)













