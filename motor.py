from pyb import Pin, Timer
  
class Motor:

    def __init__(self, PWM, DIR, nSLP, timer, channel):
        #Initializes a Motor Object
        self.nSLP_pin  = Pin(nSLP, mode=Pin.OUT_PP, value=0) 
        self.DIR_pin = Pin(DIR, mode = Pin.OUT_PP)
        self.PWM_pin = Pin(PWM)

        self.timer = Timer(timer, freq = 20000)
        self.channel = self.timer.channel(channel, mode = Timer.PWM, pin = self.PWM_pin)


    def set_effort(self, effort):
        #Sets the present effort requested from the motor based on an input value
        # between -100 and +100 (sign indicates direction)
        
        #This line ensures the effort is within the allowed range. 
        effort = max(-100, min(100, effort))

        #This line processes the sign of the effort value as a direction for the motor.
        if effort < 0:
            # This line indicates the direction of the motor
            self.DIR_pin.high()
            # This line basically turns the effort value back to positive to be used for duty cycle (absolute value)
            duty_cycle = -effort
        else:
            self.DIR_pin.low()
            # Since the effort was > 0, the value is already positive so, effort can be used directly for the duty cycle
            duty_cycle = effort
        
        self.channel.pulse_width_percent(duty_cycle)

    # Some labmates I spoke to ignore using sleep mode altogether.
    # We want sleep mode for power conservation and reducing heat and noise.
    
    def enable(self):
        # Enables the motor driver by taking it out of sleep mode (low -> high) into break mode
        self.nSLP_pin.high()
        self.set_effort(0)

    def disable(self):
        # Disables the motor driver by taking it into sleep mode
        self.nSLP_pin.low()




