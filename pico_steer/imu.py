import i2c
import bno055
from micropython import const
import threading
import time


BNO055_ADDRESS0 = const(0x28)
BNO055_ADDRESS1 = const(0x29)

class IMU():
    def __init__(self, debug):
        i2c_ = i2c.I2C()

        devices = i2c_.scan()
        self.address = 0
        self.device = None
        self.poll_delay = 0.01
        if BNO055_ADDRESS0 in devices:
            self.address = BNO055_ADDRESS0
            self.device = bno055.BNO055(i2c_, self.address, debug)
        elif BNO055_ADDRESS1 in devices:
            self.address = BNO055_ADDRESS1
            self.device = bno055.BNO055(i2c_, self.address, debug)
        
        if self.address and self.device:
            threading.Thread(target=self.poll, args=(debug,)).start()

        
    def poll(self, debug):
        while True:
            self.device.read()
