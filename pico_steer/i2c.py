from machine import I2C, Pin
from micropython import const

_i2c = None

class I2C():
    def __init__(self):
        if not _i2c:
            self.init()

    def init(self):
        _i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)

    def write(self, address, register, data):
        _i2c.writeto_mem(address, register, data)

    def read(self, address, register, length=1):
        return _i2c.readfrom_mem(address, register, length)

    def scan(self):
        return _i2c.scan()
