from micropython import const
import time
import struct
import pico_steer.debug as db

_CONVERSION_REGISTER = const(0x00)
_CONFIG_REGISTER = const(0x01)
_CONFIGURATION = const(0b0100_0100_1010_0011)

class ADS1115():
    def __init__(self, i2c, address, debug=False):
        self.i2c = i2c
        self.address = address 
        self.debug = debug

        self.i2c.writeto_mem(self.address, _CONFIG_REGISTER, bytearray([0b0100_0010, 0b1010_0011]))
        time.sleep(0.1)
        if debug:
            db.write('ADS1115 configuration {}'.format(self.i2c.readfrom_mem(self.address, _CONFIG_REGISTER, 2)))

    def read(self):
        data = self.i2c.readfrom_mem(self.address, _CONVERSION_REGISTER, 2)
        return struct.unpack('>h', data )[0]
