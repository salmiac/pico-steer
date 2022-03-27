from machine import I2C, Pin
import pico_steer.bno055
from micropython import const
import time
import pico_steer.quaternion
import pico_steer.debug as db


BNO055_ADDRESS0 = const(0x28)
BNO055_ADDRESS1 = const(0x29)

class IMU():
    def __init__(self, debug=False):
        if debug:
            db.write('Starting IMU')
        self.i2c = self.init_i2c()
        self.debug = debug
        devices = self.i2c.scan()
        address = 0
        self.device = None
        self.poll_delay = 1 # 0.01
        if BNO055_ADDRESS0 in devices:
            address = BNO055_ADDRESS0
        elif BNO055_ADDRESS1 in devices:
            address = BNO055_ADDRESS1
        if address:
            self.device = pico_steer.bno055.BNO055(self.i2c, address, debug)
        if debug:
            db.write('Imu address and device {} {}'.format(address, self.device) )

    def init_i2c(self):
        return I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)

    def read(self):
        if self.device:
            qn = None
            try:
                qn = self.device.quaternion()
            except OSError as err:
                if self.debug:
                    db.write(str(err))
            if qn is None:
                return None
            else:
                (qw, qx, qy, qz) = qn
            if self.debug:
                db.write('Quaternion {} {} {} {}'.format(qw, qx, qy, qz) )
            (heading, roll, pitch) = pico_steer.quaternion.quaternion_to_euler(qw, qx, qy, qz, self.debug)
            if self.debug:
                db.write('Heading {}, roll {}, pitch {}'.format(heading, roll, pitch) )
            return (heading, roll, pitch)
        return None
