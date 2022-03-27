import _thread
import sys
from micropython import const, kbd_intr
import pico_steer.debug as db
import struct

from machine import Pin

_SOURCE_AGIO = const(0x7f)

_HELLO = const(0xc7)
_LATLON = const(0xd0)
_AGIOTRAFFIC = const(0xd2)
_IMU = const(0xd3)
_IMU_DETACH_REQ = const(0xd4)
_NMEA_BYTES = const(0xd5)
_SWITCH_CONTROL = const(0xea)
_MACHINE_CONFIG = const(0xee)
_RELAY_CONFIG = const(0xec)
_MACHINE_DATA = const(0xef)
_STEER_CONFIG = const(0xfb)
_STEERSETTINGS = const(0xfc)
_FROM_AUTOSTEER = const(0xfd)
_AUTOSTEER_DATA = const(0xfe)

pgn_text = {
    _HELLO: 'Hello???',
    _LATLON: 'LatLon',
    _AGIOTRAFFIC: 'AgIOTraffic',
    _IMU: 'IMU',
    _IMU_DETACH_REQ: 'IMU Detach Req',
    _NMEA_BYTES: 'NMEA bytes',
    _SWITCH_CONTROL: 'switchControl',
    _MACHINE_CONFIG: 'machineConfig',
    _RELAY_CONFIG: 'relayConfig',
    _MACHINE_DATA: 'machineData',
    _STEER_CONFIG: 'steerConfig',
    _STEERSETTINGS: 'steerSettings',
    _FROM_AUTOSTEER: 'fromAutoSteer',
    _AUTOSTEER_DATA: 'autoSteerData',
}

pgn_data = {
    _HELLO: # Hello???
    lambda data: { 
    },
    _LATLON: # LatLon
    lambda data: { 
        'Latitude': struct.unpack('<i', data[0:4])[0],
        'Longitude': struct.unpack('<i', data[0:4])[0],
    },
    _AGIOTRAFFIC: # AgIOTraffic
    lambda data: { 
        'Seconds': data[0],
    },
    _IMU: # IMU
    lambda data: { 
        'Heading': struct.unpack('<h', data[0:2])[0]/10.0,
        'Roll': struct.unpack('<h', data[2:4])[0]/10.0
    },
    _IMU_DETACH_REQ: # IMU Detach Req
    lambda data: { # Removed ?
    },
    _NMEA_BYTES: # NMEA bytes
    lambda data: { # ???
    },
    _SWITCH_CONTROL: # switchControl
    lambda data: { 
        'Main': data[0],
        'Res1': data[1],
        'Res2': data[2],
        '# sections': data[3],
        'On Group 0': bin(data[4])[2:],
        'Off Group 0': bin(data[5])[2:],
        'On Group 1': bin(data[6])[2:],
        'Off Group 1': bin(data[7])[2:],
    },
    _MACHINE_CONFIG: # machineConfig
    lambda data: { 
        'raiseTime': data[0],
        'lowerTime': data[1],
        'hydEnable': data[2],
        'set0': data[3],
        'User1': data[4],
        'User2': data[5],
        'User3': data[6],
        'User4': data[7]
    },
    _RELAY_CONFIG: # machineConfig
    lambda data: { 
        'Pin 1': data[0],
        'Pin 2': data[1],
        'Pin 3': data[2],
        'Pin 4': data[3],
        'Pin 5': data[4],
        'Pin 6': data[5],
        'Pin 7': data[6],
        'Pin 8': data[7],
        'Pin 9': data[8],
        'Pin 10': data[9],
        'Pin 11': data[10],
        'Pin 12': data[11],
        'Pin 13': data[12],
        'Pin 14': data[13],
        'Pin 15': data[14],
        'Pin 16': data[15],
        'Pin 17': data[16],
        'Pin 18': data[17],
        'Pin 19': data[18],
        'Pin 20': data[19],
        'Pin 21': data[20],
        'Pin 22': data[21],
        'Pin 23': data[22],
        'Pin 24': data[23]
    },
    _MACHINE_DATA: # machineData
    lambda data: { 
        'uturn': data[0],
        'Speed': data[1]/10.0,
        'hydLift': data[2],
        'Tram': data[3],
        'Geo Stop': data[4],
        'SC': struct.unpack('<H', data[6:8])[0],
    },
    _STEER_CONFIG: # steerConfig
    lambda data: { 
        'set0': data[0],
        'invertWas': data[0] & 1,
        'steerInvertRelays': data[0] >> 1 & 1,
        'invertSteer': data[0] >> 2 & 1,
        'conv': 'Single' if data[0] >> 3 & 1 else 'Differential',
        'motorDrive': 'Cytron' if data[0] >> 4 & 1 else 'IBT2',
        'steerEnable': 'Switch' if data[0] >> 5 & 1 else ('Button' if data[0] >> 6 & 1 else 'None'),
        'encoder': data[0] >> 7 & 1,
        'pulseCount': data[1],
        'minSpeed': data[2],
        'sett1': data[3],
        'danfoss': data[3] & 1,
        'pressureSensor': data[3] >> 1 & 1,
        'currentSensor': data[3] >> 2 & 1,
    },
    _STEERSETTINGS: # steerSettings
    lambda data: { 
        'gainP': data[0],
        'highPWM': data[1],
        'lowPWM': data[2],
        'minPWM': data[3],
        'countsPerDeg': data[4],
        'steerOffset': struct.unpack('<h', data[5:7])[0]/100.0,
        'ackermanFix': data[7],
    },
    _FROM_AUTOSTEER: # fromAutoSteer
    lambda data: { 
        'ActualSteerAngle': struct.unpack('<h', data[0:2])[0]/100.0,
        'IMU Heading Hi/Lo': struct.unpack('<h', data[2:4])[0]/10.0,
        'IMU Roll Hi/Lo': struct.unpack('<h', data[4:6])[0]/10.0,
        'Switch': data[6],
        'PWMDisplay': data[7],
    },
    _AUTOSTEER_DATA: # autoSteerData
    lambda data: { 
        'Speed': struct.unpack('<H', data[0:2])[0]/10.0,
        'Status': data[2],
        'SteerAngle': struct.unpack('<h', data[3:5])[0]/100.0,
        'SC': struct.unpack('<H', data[6:8])[0],
    },
}

class Reader():
    def __init__(self, debug=False) -> None:
        self.stop = False
        self.debug = debug
        self.pgns = []
        self.payloads = []
        self.lock = _thread.allocate_lock()

    def reader(self):
        if self.debug:
            db.write('Start reader')
        kbd_intr(-1)
        while not self.stop:
            index = 0
            pgn = 0
            length = 0
            data = bytearray()
            crc_sum = 0
            while True:
                chars = sys.stdin.buffer.read(1)
                for c in chars:
                    if self.debug:
                        db.write(' C: {} {} '.format(c, index))

                    if index == 0:
                        if c == 0x80:
                            index = 1
                        continue
                    if index == 1:
                        if c == 0x81:
                            index = 2
                        else:
                            index = 0
                        continue
                    if index == 2:
                        if c == _SOURCE_AGIO:
                            index = 3
                            crc_sum += c
                        else:
                            index=0
                        continue
                    if index == 3:
                        if c in pgn_text:
                            pgn = c
                            index = 4
                            crc_sum += c
                        else:
                            index = 0
                        continue
                    if index == 4:
                        length = c
                        index = 5
                        crc_sum += c
                        continue
                    if index >= 5 and index < length + 5:
                        data.append(c)
                        index += 1
                        crc_sum += c
                        continue
                    if index == 5 + length:
                        crc_sum %= 256
                        if crc_sum == c:
                            try:
                                payload = pgn_data[pgn](data)
                            except Exception as err:
                                if self.debug:
                                    db.write(' *lambda feili* ')
                                    db.write(str(err))
                                return
                            self.lock.acquire()
                            self.pgns.append(pgn)
                            self.payloads.append(payload)
                            self.lock.release()
                            if self.debug:
                                db.write(' pgn {}, payload {}'.format(pgn, payload))
                    index = 0
                    pgn = 0
                    length = 0
                    data = bytearray()
                    crc_sum = 0
        kbd_intr(3)
