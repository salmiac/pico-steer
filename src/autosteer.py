import time

import pico_steer.imu
import pico_steer.agio
import pico_steer.settings
import pico_steer.motor_control
import pico_steer.was
import pico_steer.debug as db
from machine import Pin
import micropython
import sys
import gc

stop = Pin(15, Pin.IN, Pin.PULL_UP)
work_switch = Pin(12, Pin.IN, Pin.PULL_UP)
activity_led = Pin(17, Pin.OUT, Pin.OPEN_DRAIN)
internal_activity_led = Pin(25, Pin.OUT)
internal_activity_led.toggle()

if stop.value() == 0:
    sys.exit()

internal_activity_led.toggle()
debug=False

if debug:
    db.write('Start autosteer.')

imu = pico_steer.imu.IMU(debug=debug)
internal_activity_led.toggle()
settings = pico_steer.settings.Settings(debug=debug)
internal_activity_led.toggle()
was = pico_steer.was.WAS(settings, debug=False)
internal_activity_led.toggle()
motor_control = pico_steer.motor_control.MotorControl(settings, debug=debug)
internal_activity_led.toggle()
agio = pico_steer.agio.AgIO(settings, motor_control, debug=debug)
internal_activity_led.toggle()

blinker = 0

agio.start_reader()
internal_activity_led.toggle()

if debug:
    db.write('Start loop.')

while True:
    blinker += 1
    agio.read()
    imu_reading = imu.read()
    wheel_angle = was.read()

    if imu_reading is not None and wheel_angle is not None:
        (heading, roll, pitch) = imu_reading
        motor_control.update_motor(wheel_angle)
        if motor_control.switch_active:
            switch = 0b1111_1101
        else:
            switch = 0b1111_1111
        if work_switch.value() == 0:
            switch &= 0b1111_1110
        
        agio.from_autosteer(wheel_angle, heading, roll, switch, motor_control.pwm_display())
    else:
        agio.alive()
    time.sleep(0.01)
    if blinker % 32 == 0:
        if debug:
            db.write('.')
        activity_led.toggle()
        internal_activity_led.toggle()
    if stop.value() == 0:
        micropython.kbd_intr(3)
        agio.reader.stop=True
        break
    gc.collect()
