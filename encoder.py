from time import ticks_us, ticks_diff # Use to get dt value in update()
from pyb import Pin, Timer


class Encoder:
    # A quadrature encoder decoding interface encapsulated in a Python class

    def __init__(self, tim, chA_pin, chB_pin):

        # initializes an Encoder object
        self.position   = 0 # Total accumulated position of the encoder
        self.prev_count = 0 # Counter values from the most recent update
        self.delta      = 0 # Change in count between last two updates
        self.dt         = 0 # Amount of time between last two updates
        self.last_time = ticks_us()
        
        ENC_timer = Timer(tim, period = 0xFFFF, prescaler = 0)
        self.ENC_timer = ENC_timer
         
        self.ENC_chA = ENC_timer.channel(1, pin=Pin(chA_pin), mode=Timer.ENC_AB) # Encoder 1 (Timer 1)
        self.ENC_chB = ENC_timer.channel(2, pin=Pin(chB_pin), mode=Timer.ENC_AB) # Encoder 1 (Timer 2)

        
    def update(self):
        # Runs one update step on the encoder's timer counter to keep track 
        #   of the change in count and check for counter reload

        #Each time the encoder turns, it generates a series of digital pulses. 
        # The timer counts these pulses, and the driver accumulates the difference 
        # in counts on each update
        count = self.ENC_timer.counter()
        now = ticks_us()

        self.delta = count - self.prev_count


        # Delta subtracts current count from the previous count to see the difference. 
        # Almost always gonna be small distances
        # Cases when the encoder reaches the value 65535 resets to zero which will give us bad readings
        # Overflow/Underflow cases accounts solely for that big jump (>32767). 
        # If the jump is higher than 32767, it is most likely moving from 0-65535, therefore correction 
        # cases activate.
        
        if self.delta > 32767:  # Overflow case
            self.delta -= 65536
        elif self.delta < -32767:  # Underflow case
            self.delta += 65536

        self.position += self.delta
        self.prev_count = count
        self.dt = ticks_diff(now, self.last_time) / 1_000_000
        self.last_time = now
        
        print(f"Encoder Update: dt = {self.dt}, Delta = {self.delta}")
        
        pass

    def get_position(self):
        # Returns the most recently updated value of position as determined
        #   within the update() method
        
        # we know 1440 counts equals one full revolution (2pi).
        self.position_radians = self.position #* 2 * 3.14/1440 

        return self.position_radians # Not in radians anymore, this is in ticks
    
    def get_velocity(self): # angular velocity!! 
        
        # Returns a measure of velocity using the most recently updated value
        #   of delta as determined wihin the update() method
        if self.dt == 0:
            return 0
        
        print(f"Raw delta before negation: {self.delta}")

        velocity = (self.delta * 2 * 3.14 / 1440) / self.dt # [rad/s] !!!

        return velocity
    


    def zero(self):

        # Sets the present encoder position to zero and causes future updates 
        #   to measure with respect to the new zero position
        self.position = 0
        self.prev_count = 0
        self.count = 0
        self.velocity = 0
        self.position_radians = 0
        self.ticks = 0

        self.prev_count = 0
        self.position = 0
        self.delta = 0
        self.true_position = 0
        self.true_delta = 0
        self.velocity = 0
        self.ticks = 0

        pass
