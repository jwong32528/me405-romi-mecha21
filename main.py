import cotask
from motor import Motor
from encoder import Encoder
from controls import Controls
from linesensor import LineSensor
from BNO055 import BNO055
from pyb import ADC, Pin, I2C
from task_share import Share
import math
import button_handler
from task_IMU import task_imu
from task_encoder import task_encoder

# !!! Fix the connections for these
from task_line_sensor import task_line_sensor
from task_controls import task_controls
   
# !!! Not used
from task_closed_loops import task_closed_loop_left, task_closed_loop_right
import bump
from utils import normalize_error
   

def main():
    
    ### Properties
    # Line Following Mode
    Kp =    5
    Ki =    0.15
    Kd =    0.05
    
    # Stright Mode (Only used with the closed_loop tasks activated)
    Kp_2 =  4
    Ki_2 =  0.0000005
    Kd_2 =  0.00
    
    # ADD THIS (KEEP CONSISTENT IN CONTROLS.PY) Pivot (Heading) Mode
    Kp_3 = 1.5
    Ki_3 = 0
    Kd_3 = 0.1
    
    #wheel_radius = 0.035 # [m]
    #V_ref_mps = 0.22 # [m/s]
    V_ref_rad = 2 * math.pi #V_ref_mps / wheel_radius # [rad/s] 
    
    # Pivot Mode Max Speed
    pivot_max_effort = 15
    
    # Base Effort Tuning (When not using closed_loop_left/right)
    left_base_effort = 15
    right_base_effort = 16.5
    

    ### Initialize Shares
    #IMU Heading Share
    heading_share = Share('f')
    datum_share = Share('f')
    
    # Encoder Data Share
    left_position_share = Share('f')
    right_position_share = Share('f')
    left_velocity_share = Share('f')
    right_velocity_share = Share('f')
    
    left_dt_share = Share('f')
    right_dt_share = Share('f')
    
    grid_share = Share('f')
    grid_share.put(0)
    
    # Centroid Share
    centroid_share = Share('f')
    
    # Shows battery level before starting
    ADC_bat = ADC(Pin('C0'))
    bat_level = ADC_bat.read() * 3.3/4095 * 14.7/4.7
    
    # Motor Effort Share
    left_effort_share = Share('f')   # 'f' is for floats
    right_effort_share = Share('f')
    
    # Mode Share
    mode_share = Share('f') # short integer
    mode_share.put(0) # S0_LINE_FOLLOW_MODE
    
    # Battery Voltage Share
    battery_voltage_share = Share('f')
    battery_voltage_share.put(bat_level)
    
    print(f"Current Battery Voltage: {bat_level}")
    
    
    ### Press the nucleo user button to start the program
    print("Press the Nucleo button to start Romi")
    while not button_handler.button_pressed(button_handler.nucleo_button):
        pass
    
    
    ### Initialize Sensors
    # Initialize Line Sensor with Fixed Calibration Data
    sensor = LineSensor(mode_share)

    # Initialize IMU
    i2c = I2C(1, I2C.MASTER, baudrate=400000)
    imu = BNO055(i2c)
    imu.set_mode(0x0C)  # Set to NDOF (fusion mode)
    
    # Initialize and Enable Motors
    left_motor = Motor("PA0", "PA10", "PB10", 2, 1)
    right_motor = Motor("PA1", "PB4", "PB5", 2, 2)
    
    left_motor.enable()
    right_motor.enable()
    
    # Initialize encoders
    left_encoder = Encoder(tim=1, chA_pin="PA8", chB_pin="PA9")   
    right_encoder = Encoder(tim=3, chA_pin="PA6", chB_pin="PA7") 

    # Initialize controls
    controls = Controls(Kp, Ki, Kd, V_ref_rad, V_ref_rad, Kp_2, Ki_2 , Kd_2,
                        Kp_3, Ki_3, Kd_3, pivot_max_effort, left_base_effort, 
                        right_base_effort, sensor=sensor, 
                        battery_voltage_share = battery_voltage_share, 
                        left_encoder = left_encoder, 
                        right_encoder = right_encoder,
                        left_motor = left_motor, right_motor = right_motor,
                        centroid_share = centroid_share)        

    ### Create tasks
    task_line = cotask.Task(task_line_sensor, name="Line Sensor", priority = 1, 
                           period = 10, shares=(sensor, centroid_share, grid_share, 
                                                mode_share))

    
    task_cont = cotask.Task(task_controls, name="Adjust Speed", priority=1, 
                           period = 10, shares=(controls, left_effort_share, 
                                              right_effort_share, 
                                              left_dt_share, right_dt_share, 
                                              left_position_share, 
                                              right_position_share,
                                              left_velocity_share, 
                                              right_velocity_share, heading_share,
                                              datum_share, mode_share))
    
    task_enco = cotask.Task(task_encoder, name = "Encoder Data", priority = 1, 
                           period = 10, shares = (left_encoder, right_encoder, 
                                                  left_position_share, 
                                                  right_position_share, 
                                                  left_velocity_share, 
                                                  right_velocity_share,
                                                  left_dt_share,
                                                  right_dt_share, grid_share, mode_share))
    
    task_head = cotask.Task(task_imu, name = "IMU Task", priority = 1,
                            period = 10, shares = (imu, heading_share, datum_share, mode_share))
    
    #task_left = cotask.Task(task_closed_loop_left, name="Left Motor", 
    #                        priority=1, period= 50, shares=(controls, 
    #                                                         left_effort_share, 
    #                                                         left_velocity_share,
    #                                                         left_dt_share,
    #                                                         left_position_share))
    
    #task_right = cotask.Task(task_closed_loop_right, name="Right Motor", 
    #                         priority=1, period=50, shares=(controls, 
    #                                                         right_effort_share,
    #                                                         right_velocity_share,
    #                                                         right_dt_share,
    #                                                         right_position_share))
    
    #task3 = cotask.Task(task_adjust_speed, name="Adjust Speed", priority=1, period=10, shares=(controls, left_effort_share, right_effort_share))

    ### Add tasks to scheduler
    cotask.task_list.append(task_enco)
    cotask.task_list.append(task_head)
    cotask.task_list.append(task_line)
    cotask.task_list.append(task_cont)
    

    

    ### Run the scheduler
    while True:
        
        
        cotask.task_list.pri_sched()
        
    
if __name__ == "__main__":
    main()

