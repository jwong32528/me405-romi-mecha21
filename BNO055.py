#import motor
#import struct
from micropython import const
from struct import calcsize, unpack, pack
from pyb import I2C

class BNO055:
    #This class facilitates interaction between the BNO055 IMU using
    # I2C communication
    
    DEV_ADDR = const(0x28)
    
    # Similar to Pin(Pin.cpu.XX, Pin.OUT)
    class reg:
        EUL_HEADING_MSB     =   (const(0x1B), b"<B")
        EUL_HEADING_LSB     =   (const(0x1A), b"<B")
        EUL_HEADING         =   (const(0x1A), b"<h")
        EUL_DATA_ALL        =   (const(0x1A), b"<hhh")
        GYR_DATA_ALL        =   (const(0x14), b"<hhh")
        CALIBRATION_STATUS  =   (const(0x35), b"B")
        OPR_MODE            =   (const(0x3D), b"B")
        CALIBRATION_DATA    =   (const(0x55), "22B")
    
    
    def __init__(self, i2c: I2C):
        
        # Register Addresses
        self._i2c = i2c
        self._buf = bytearray((0 for n in range(22)))
        
        
    def _read_reg(self, reg):
        
        #Determine number of bytes to read
        length = calcsize(reg[1])
        
        #Create a memoryview object of the right size
        buf = memoryview(self._buf)[:length]
        
        #Read from the I2C bus into the memoryview
        self._i2c.mem_read(buf, self.DEV_ADDR, reg[0])
        
        #Unpack the bytes into a tuple
        return unpack(reg[1], buf)
    
    
    def _write_reg(self, reg, values):
        
        if not isinstance(values, (tuple, list)):
            values = (values,)
        data = pack(reg[1], *values)
        self._i2c.mem_write(data, self.DEV_ADDR, reg[0])
    
    
    def euler(self):
        
        """
        Read Euler angles from the IMU to use as measurements for feedback
        
        """
        head, roll, pitch = self._read_reg(BNO055.reg.EUL_DATA_ALL)
        return (head/16, roll/16, pitch/16)
    
    
    def set_mode(self, mode):
        
        """
        # Change the the operating mode of the IMU to one of the many 
        "fusion" modes availible from the BNO055
        
        """
        
        self._write_reg(BNO055.reg.OPR_MODE, mode)
        
        
    def get_calibration_status(self):
        
        """
        Retrieve and parce the calibration status byte from the IMU
        
        """
        status = self._read_reg(BNO055.reg.CALIBRATION_STATUS)[0]
        
        return {
            
            'sys': (status >> 6) & 0x03,
            'gyro': (status >> 4) & 0x03,
            'accel': (status >> 2) & 0x03,
            'mag': status & 0x03
            
        }
        

    def get_calibration_data(self):
        
        """
        Retrieve the calibration coefficients from the IMU as binary data
        
        """
        
        length = 22
        buf = bytearray(length)
        self._i2c.mem_read(buf, self.DEV_ADDR, BNO055.reg.CALIBRATION_DATA[0])
        return buf


    def set_calibration_data(self, data: bytearray):
        
        """
        Write calibration coefficients back to the IMU from pre-recorded 
        binary data
        
        """
        
        if len(data) != 22:
            raise ValueError("Calibration data should be 22 bytes long")
        
        self._i2c.mem_write(data, self.DEV_ADDR, BNO055.reg.CALIBRATION_DATA[0])
        
        
    def angular_velocity(self):
        
        """
        Reads angular velocity from the IMU to use as measurements for 
        feedback
        
        :return: Tuple of (gx, gy, gz) in (assumed) degrees per second.
        
        """
        
        gx, gy, gz = self._read_reg(BNO055.reg.GYR_DATA_ALL)
        # Conversion factor may need adjustment based on the datasheet; using /16 as a placeholder.
        return (gx / 16.0, gy / 16.0, gz / 16.0)

"""
import motor
import struct
from pyb import I2C, Pin

class BNO055:

    def __init__(self,I2C):
        # Register Addresses
        self.MAG_RADIUS_MSB = 0x6A
        self.MAG_RADIUS_LSB = 0x69

        self.ACC_RADIUS_MSB = 0x68
        self.ACC_RADIUS_LSB = 0x67

        self.GYR_OFFSET_Z_MSB = 0x66
        self.GYR_OFFSET_Z_LSB = 0x65
        self.GYR_OFFSET_Y_MSB = 0x64
        self.GYR_OFFSET_Y_LSB = 0x63
        self.GYR_OFFSET_X_MSB = 0x62
        self.GYR_OFFSET_X_LSB = 0x61

        self.MAG_OFFSET_Z_MSB = 0x60
        self.MAG_OFFSET_Z_LSB = 0x5F
        self.MAG_OFFSET_Y_MSB = 0x5E
        self.MAG_OFFSET_Y_LSB = 0x5D
        self.MAG_OFFSET_X_MSB = 0x5C
        self.MAG_OFFSET_X_LSB = 0x5B

        self.ACC_OFFSET_Z_MSB = 0x5A
        self.ACC_OFFSET_Z_LSB = 0x59
        self.ACC_OFFSET_Y_MSB = 0x58
        self.ACC_OFFSET_Y_LSB = 0x57
        self.ACC_OFFSET_X_MSB = 0x56
        self.ACC_OFFSET_X_LSB = 0x55

        self.CHIP_ID = 0x00
        self.ACC_ID = 0x01
        self.MAG_ID = 0x02
        self.GYRO_ID = 0x03
"""



 