import time
import pico_steer.pwm_motor as pwm
from machine import Pin
import pico_steer.debug as db

ANGLE_GAIN = 1 # 10 degrees = full power * gain %

class MotorControl(): 
    def __init__(self, settings, debug=False):
        self.settings = settings
        self.debug = debug
        self.running = False
        self.value_changed = True
        self.direction = 1 # 1 = right, 0 = left
        self.target_angle = 0
        self.ok_to_run = False

        self.switch = Pin(13, Pin.IN, Pin.PULL_UP)
        self.switch_active = False
        self.active_led = Pin(16, Pin.OUT)
        self.active_led.on()
        self.direction_led = Pin(14, Pin.OUT)
        self.direction_led.on()
        self.pwm_value = 0

    def calculate_pwm(self, wheel_angle):
        delta_angle = self.target_angle - wheel_angle
        pwm_value = delta_angle * self.settings.settings['gainP'] * ANGLE_GAIN
        if pwm_value < 0:
            pwm_value = -pwm_value
            direction = 1 if self.settings.settings['invertSteer'] else 0
        else:
            direction = 0 if self.settings.settings['invertSteer'] else 1
        if pwm_value > self.settings.settings['highPWM'] / 2.55:
            pwm_value = self.settings.settings['highPWM'] / 2.55
        if pwm_value < self.settings.settings['minPWM'] / 2.55:
            pwm_value = self.settings.settings['minPWM'] / 2.55
        if self.pwm_value != pwm_value or direction != self.direction:
            self.value_changed = True
            self.pwm_value = pwm_value
            self.direction = direction

    def update_motor(self, wheel_angle):
        if self.debug:
            db.write('Start motor controller.')
        self.active_led.value(self.switch.value())
        start = False
        stop = False

        self.switch_active = False if self.switch.value() else True
        if self.switch_active and not self.running and self.ok_to_run:
            start = True
        if self.running and (not self.switch_active or not self.ok_to_run):
            stop = True

        if self.running or start:
            self.calculate_pwm(wheel_angle)
        if stop:
            if self.debug:
                db.write('Stop!')
            pwm.stop()
            self.pwm_value = 0
            self.running = False
            return
        if self.value_changed:
            self.value_changed = False
            if self.debug:
                db.write('Set: pwm: {}, switch: {}, direction: {}'.format(self.pwm_value, self.switch_active, self.direction))
            pwm.update(self.pwm_value, self.direction)
            self.direction_led.value(self.direction)
        if start:
            if self.debug:
                db.write('Start!')
            pwm.start()
            self.running = True

    def set_control(self, auto_steer_data):
        # auto_steer_data['Speed']
        # auto_steer_data['Status']
        # auto_steer_data['SteerAngle']
        # auto_steer_data['SC']
        self.target_angle = auto_steer_data['SteerAngle']

        if auto_steer_data['Status']:
            self.ok_to_run = True
        else:
            self.ok_to_run = False

    def pwm_display(self):
        return int(self.pwm_value * 2.55)
