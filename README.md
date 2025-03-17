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
The Romi Time-Trial project focuses on completing the game track using various sensors for feedback and controls. The primary objectives include:
- Developing a robust **line-following algorithm**.
- Ensuring **fast and consistent** lap times.
- Overcoming hardware and software challenges encountered during development.

## Mechanical and Electrical Design

### Design Overview
For the mechanical components of our Romi, we used a line sensor, two bump sensors, and an IMU. The line sensor was securely mounted directly onto the Romi’s chassis, positioned as low as possible without touching the ground to minimize reading errors. The IMU was mounted underneath the front of the chassis, while the bump sensors were attached to the front of the Romi.  
![alt text](https://github.com/jwong32528/me405-romi-mecha21/blob/pictures/romi.jpg)
*Romi Robot*

### **Hardware Components:**
- **Motors:** Romi Motor 4.5 V
- **Sensors:** QTRX-HD-15A Reflectance Sensor Array, BNO055 IMU, Bump Sensors, Encoders
- **Microcontroller:** NUCLEO-L476RG (STM32L476RG MCU)
- **Power Supply:** 6 X AA Batteries
- **MISC:** Voltage Divider Attachment (For Voltage reading)

### **Wiring and Assembly:**
- Complete **Wiring Diagram Excel** is attached in the repository

![alt text](https://github.com/jwong32528/me405-romi-mecha21/blob/pictures/wiring_diagram.png)  
*Wiring Diagram*

### **Design:**
- Sensor placement optimization for **improved track detection**
  - IR Sensor placed on the front of Romi to process feedback quickly
  - IR Sensor placed as close to the ground as possible to reduce errors
  - Bump Sensors placed on the front-most part of Romi to ensure the sensor is triggered when bumping into walls
  - IMU mounted under the chassis to reduce clutter.
- Custom **mounting brackets** for sensor stability
  - Standoffs


## 4. Software and Control Implementation

### Software Overview

The main.py file is responsible for initializing and managing the core components of the Romi. It initializes the IMU, encoders, motors, and line sensor, and all the shared variables for communication between tasks, including the controller gains. The program initializes the encoder, IMU, linesensor, and controls tasks, appending the tasks to the scheduler, and running them at a 10 ms interval. 

The controls task implements a finite state machine to change its state between line following, pivot, straight distance, and finish line mode. The controls task also implements three queues to hard code the linear displacement, angle displacement, and supervisor directions, so that Romi is not only able to complete this term's track, but also future iterations of the track with minimal change to our overall code structure.
 
The encoder task acquires the current velocity and position. We chose not to convert the encoder ticks directly to [rad/s] and instead multiplied the encoder resolution of 1440 counts/rev by the number of desired wheel rotations to get the target distances. 

The linesensor task gets the sensor readings and normalizes the data so that white = 0 and black = 1, returning the centroid for line tracing. 
The IMU task acquires the heading data, which allows us to know the orientation of Romi at all times but with some error.  

![alt text](https://github.com/jwong32528/me405-romi-mecha21/blob/pictures/task_diagram.jpg)
*Task Diagram*  
We used the task diagram shown above to structure our code and the finite state machine for the controls task. The closed loop tasks are crossed out because we did not have enough time to implement the velocity controller with the line tracing controller. If we had more time, we would program Romi so that it only uses the velocity controller during the grid section of the game track to prevent Romi from slightly turning while moving forward.

### **Programming Language and Libraries:**
- Python 3.9

### **Classes:**
**Main**
- **Motor**: Initializes the motors, allowing for easy enabling/disabling, effort adjustments, and direction changes
- **Encoder**: Initializes the encoders, reads tick counts, and converts them into position and velocity measurements
- **Linesensor**: Reads and normalizes sensor data, then returns the centroid for line tracing
- **Controls**: Implements a basic PID controller for line tracing using centroid data
- **Bumpsensor**: Detects a bump
- **Button handler**: Uses the button on the romi to run the romi
- **Imu**: Acquires heading data from the magnetometer to know the orientation of the Romi

**Utility**
- **Cotask**: Manages cooperative multitasking, allowing multiple tasks to run efficiently
- **Taskshare**: Facilitates data sharing between tasks, ensuring smooth communication
- **Cqueue**: Implements a queue structure for task scheduling and data handling
- **Linesensor Calibration**: Calibrates the linesensor for black and white surfaces
- **Imu Calibration**: Calibrates the IMU to correct for sensor drift and improve heading accuracy
- **Utils**: Functions to reduce the amount of code in a file

### **Control System Overview:**
The robot implements a **PID control controller** to adjust motor speeds based on sensor feedback. 
- **Receives data from the line sensor and normalizes the data to output a centroid**
- **Romi uses the centroid to trace the lines on the game track**
- **Gains were tuned iteratively through trial and error**


### **State Machine / Task Flow:**
- **Line Following:** PID controller that adjusts the left and right wheel effort values based on the line sensor task's centroid value. Romi follows the line indefinitely until it detects a bump or a task switches the mode.
- **Pivot Mode:** Uses IMU to measure initial heading as reference for rotating Romi based on a fixed angle displacement. 
- **Straight Mode:** Uses encoder to measure the current position. The desired displacement is then acquired from the queue and added to the current position to obtain a target distance. Romi moves forward until the current encoder distance reaches the target distance.
- **Finish Line Mode:** Romi idles



## Challenges
The most challenging part of the game track was navigating the diamond section. The sharp turns made it difficult for Romi to stay on the line without veering off. To overcome this challenge, we programmed Romi to go straight through the diamond when the Romi detected the diamond.   
Another challenge was integrating both the PID controllers for line tracing and straight-line movement. Running both controllers simultaneously caused the velocity PID controller to adjust the velocity, even when we needed different velocities for turning. Due to time constraints and the fact that it was not essential, we decided not to incorporate the velocity controller. However, with more time, we would have implemented it specifically for the grid section to prevent the Romi from deviating from its straight path.  
If we were to redo this project, we would eliminate the use of the line sensor and instead hard-code the Romi’s movement using predefined distances and angles. We found that the line sensor becomes unreliable at higher speeds, and we could achieve the same level of consistency without it.

## Results
Out of three official attempts, only one was successful.  
We were able to complete the game track in 48 seconds during the live demo. The video below shows the Romi completing the game track using the code in the repository.

Trial 1: DNF - Romi was not properly initialized    
Trial 2: 48 [s] - 5 [s] = 43 [s]  
Trial 3: DNF - Romi deviated from its straight line path during the grid section due to the lack of a PID controller for velocity.  

**Video:**  
[![Watch the Video](https://img.youtube.com/vi/Uyyd9d3AcY4/0.jpg)](https://youtu.be/Uyyd9d3AcY4)














