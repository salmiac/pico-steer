import time

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

class BNO055():
    def __init__(self, i2c, address, debug):
        self.i2c = i2c
        self.address = address 
        self.debug = debug

        time.sleep(0.1)
        id = int.from_bytes(i2c.read(self.i2c_address, _ID_REGISTER, 1), 'little')
        print('ID', id)
        if id == 0xa0:
            self._write_config(_MODE_REGISTER, CONFIG_MODE)
            self._write_config(_POWER_REGISTER, _POWER_NORMAL)
            self._write_config(_MODE_REGISTER, IMUPLUS_MODE)
        else:
            if debug:
                print('Not BNO055 ID!')
            self.i2c_address = 0

    def _write_config(self, register, value):
        time.sleep(0.02)
        self._write(register, bytes(bytearray([value])))
        time.sleep(0.1)


    def read():

