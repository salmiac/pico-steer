from machine import I2C, Pin
import time
import pico_steer.ads1115
import pico_steer.pico_adc
import pico_steer.debug as db
from micropython import const

_ADS111X_ADDRESS0 = const(0b01001000)
_ADS111X_ADDRESS1 = const(0b01001001)
MAXANGLE = 85

class WAS():
    def __init__(self, settings, debug=False):
        self.settings = settings
        self.i2c = self.init_i2c()
        self.debug = debug
        devices = self.i2c.scan()
        address = 0
        self.device = None
        if _ADS111X_ADDRESS0 in devices:
            address = _ADS111X_ADDRESS0
        elif _ADS111X_ADDRESS1 in devices:
            address = _ADS111X_ADDRESS1
        else:
            self.device = pico_steer.pico_adc.Pico_ADC(self.debug)
        if address:
            self.device = pico_steer.ads1115.ADS1115(self.i2c, address, self.debug)

    def init_i2c(self):
        return I2C(1, scl=Pin(3), sda=Pin(2), freq=400000)

    def read(self):
        if self.device:
            adc = None
            try:
                adc = self.device.read()
            except OSError as err:
                if self.debug:
                    db.write(str(err))
            if adc is None:
                return None
            if self.debug:
                db.write('ADC {}'.format(adc))
            angle = (adc/16383.5 - 1) * 5 / 4.0 * 60.0 * self.settings.settings['countsPerDeg'] / 100.0 + self.settings.settings['steerOffset']
            if self.settings.settings['invertWas']:
                angle = -angle
            if angle < -MAXANGLE:
                angle = -MAXANGLE
            if angle > MAXANGLE:
                angle = MAXANGLE
            if self.debug:
                db.write('Angle {}'.format(angle))
            return angle
        return None
        