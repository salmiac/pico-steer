from machine import I2C, Pin
import time
from micropython import const
import struct

CONFIG_MODE = const(0x00)
ACCONLY_MODE = const(0x01)
MAGONLY_MODE = const(0x02)
GYRONLY_MODE = const(0x03)
ACCMAG_MODE = const(0x04)
ACCGYRO_MODE = const(0x05)
MAGGYRO_MODE = const(0x06)
AMG_MODE = const(0x07)
IMUPLUS_MODE = const(0x08)

_POWER_NORMAL = const(0x00)
_POWER_LOW = const(0x01)
_POWER_SUSPEND = const(0x02)

_MODE_REGISTER = const(0x3D)
_PAGE_REGISTER = const(0x07)
_ACCEL_CONFIG_REGISTER = const(0x08)
_MAGNET_CONFIG_REGISTER = const(0x09)
_GYRO_CONFIG_0_REGISTER = const(0x0A)
_GYRO_CONFIG_1_REGISTER = const(0x0B)
_QUATERNION_REGISTER = const(0x20)
_CALIBRATION_REGISTER = const(0x35)
_OFFSET_ACCEL_REGISTER = const(0x55)
_OFFSET_MAGNET_REGISTER = const(0x5B)
_OFFSET_GYRO_REGISTER = const(0x61)
_RADIUS_ACCEL_REGISTER = const(0x67)
_RADIUS_MAGNET_REGISTER = const(0x69)
_TRIGGER_REGISTER = const(0x3F)
_POWER_REGISTER = const(0x3E)
_ID_REGISTER = const(0x00)
# Axis remap registers and values
_AXIS_MAP_CONFIG_REGISTER = const(0x41)
_AXIS_MAP_SIGN_REGISTER = const(0x42)

class IMU():
    def __init__(self):

        self.i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)          # create I2C peripheral at frequency of 400kHz
                                        # depending on the port, extra parameters may be required
                                        # to select the peripheral and/or pins to use

        i2c_list = self.i2c.scan()                      # scan for peripherals, returning a list of 7-bit addresses

        for address in i2c_list:
            print('Address', hex(address))

        self.i2c_address = 0

        self.device = None

        if 0x28 in i2c_list:
            self.i2c_address = 0x28
            self.device = 'bno055'
        if 0x29 in i2c_list:
            self.i2c_address = 0x29
            self.device = 'bno055'

        if self.i2c_address:
            time.sleep(0.1)
            id = int.from_bytes(self.i2c.readfrom_mem(self.i2c_address, _ID_REGISTER, 1), 'little')
            print('ID', id)
            if id == 0xa0:
                print('Power', self.i2c.readfrom_mem(self.i2c_address, _POWER_REGISTER, 1) )
                print('Mode', self.i2c.readfrom_mem(self.i2c_address, _MODE_REGISTER, 1) )
                self._write_config(_MODE_REGISTER, CONFIG_MODE)
                self._write_config(_POWER_REGISTER, _POWER_NORMAL)
                self._write_config(_MODE_REGISTER, IMUPLUS_MODE)
                print('Power', self.i2c.readfrom_mem(self.i2c_address, _POWER_REGISTER, 1) )
                print('Mode', self.i2c.readfrom_mem(self.i2c_address, _MODE_REGISTER, 1) )
                time.sleep(0.5)
                print('All', self.i2c.readfrom_mem(self.i2c_address, _MODE_REGISTER, 32) )
                time.sleep(0.5)
                self._read(0, 16)
            else:
                self.i2c_address = 0

    def _write_config(self, register, value):
        time.sleep(0.02)
        self._write(register, bytes(bytearray([value])))
        time.sleep(0.1)

    def _write(self, register, data):
        self.i2c.writeto_mem(self.i2c_address, register, data)

    def _read(self, register, length=1):
        data = self.i2c.readfrom_mem(self.i2c_address, register, length)
        return data
        # print(data)

    def quaternion(self):
        if self.device:
            return self._read(_QUATERNION_REGISTER, 8)

imu = IMU()

for n in range(100):
    time.sleep(0.1)
    print(imu.quaternion())

# i2c.writeto(42, b'123')         # write 3 bytes to peripheral with 7-bit address 42
# i2c.readfrom(42, 4)             # read 4 bytes from peripheral with 7-bit address 42

# i2c.readfrom_mem(42, 8, 3)      # read 3 bytes from memory of peripheral 42,
                                #   starting at memory-address 8 in the peripheral
# i2c.writeto_mem(42, 2, b'\x10') # write 1 byte to memory of peripheral 42
                                #   starting at address 2 in the peripheral

