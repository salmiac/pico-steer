import struct
import sys
from micropython import const, kbd_intr
import _thread
import time
import pico_steer.serial_reader
import pico_steer.debug as db
import pico_steer.section_control

_HELLO = const(0xc7)
_LATLON = const(0xd0)
_AGIOTRAFFIC = const(0xd2)
_IMU = const(0xd3)
_IMU_DETACH_REQ = const(0xd4)
_NMEA_BYTES = const(0xd5)
_SWITCH_CONTROL = const(0xea)
_MACHINE_CONFIG = const(0xee)
_MACHINE_DATA = const(0xef)
_STEER_CONFIG = const(0xfb)
_STEERSETTINGS = const(0xfc)
_FROM_AUTOSTEER = const(0xfd)
_AUTOSTEER_DATA = const(0xfe)

class AgIO():
    def __init__(self, settings, motor_control, debug=False):
        self.settings = settings
        self.motor_control = motor_control
        self.debug = debug
        self.reader = pico_steer.serial_reader.Reader(debug)
        self.sc = pico_steer.section_control.SectionControl()

    def start_reader(self):
        _thread.start_new_thread(self.reader.reader, ())

    def alive(self):
        sys.stdout.write(bytearray([0x80,0x81, 0x7f, 0xC7, 0x01, 0x00, 0x47]))

    def from_autosteer(self, wheel_angle, heading, roll, switch, pwm_display):
        data = bytearray([0x80, 0x81, 0x7e, 0xfd, 0x08])
        wheel_angle_int = int(wheel_angle * 100)
        for b in struct.pack('<H', wheel_angle_int):
            data.append(b)
        heading_int = int(heading * 10)
        for b in struct.pack('<H', heading_int):
            data.append(b)
        roll_int = int(roll * 10)
        for b in struct.pack('<H', roll_int):
            data.append(b)

        data.append(switch)
        data.append(pwm_display)

        crc = 0
        for byte in data[2:]:
            crc += byte
        crc %= 256
        data.append(crc)
        sys.stdout.write(data)

    def read(self):
        empty = False
        while not empty:
            pgn = payload = None
            self.reader.lock.acquire()
            if len(self.reader.pgns):
                pgn = self.reader.pgns.pop(0)
                payload = self.reader.payloads.pop(0)
            else:
                empty = True
            self.reader.lock.release()

            if pgn is not None:
                if pgn == _STEER_CONFIG:
                    if self.debug:
                        db.write('steer config')
                    self.settings.settings.update(payload)
                    self.settings.save_settings()
                if pgn == _STEERSETTINGS:
                    if self.debug:
                        db.write('steer settings')
                    self.settings.settings.update(payload)
                    self.settings.save_settings()
                if pgn == _AUTOSTEER_DATA:
                    if self.debug:
                        db.write('autosteer data')
                    if payload is not None:
                        self.motor_control.set_control(payload)
                        if self.debug:
                            db.write(payload['SC'])
                        self.sc.update(payload['SC'])
