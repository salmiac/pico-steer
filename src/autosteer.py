import time

import pico_steer.imu
import pico_steer.agio
import pico_steer.settings
import pico_steer.motor_control
import pico_steer.was
import pico_steer.debug as db
from machine import Pin
import micropython
import gc

stop = Pin(15, Pin.IN, Pin.PULL_UP)
activity_led = Pin(17, Pin.OUT, Pin.OPEN_DRAIN)
internal_activity_led = Pin(25, Pin.OUT)

debug=True

imu = pico_steer.imu.IMU(debug=False)
settings = pico_steer.settings.Settings(debug=debug)
was = pico_steer.was.WAS(settings, debug=False)
motor_control = pico_steer.motor_control.MotorControl(settings, debug=False)
agio = pico_steer.agio.AgIO(settings, motor_control, debug=debug)

blinker = 0

agio.start_reader()

while True:
    blinker += 1
    agio.read()
    while True:
        imu_reading = imu.read()
        if imu_reading is not None:
            (heading, roll, pitch) = imu_reading
            break
    while True:
        wheel_angle = was.read()
        if wheel_angle is not None:
            break
    motor_control.update_motor(wheel_angle)
    if motor_control.switch_active:
        switch = 0x00
    else:
        switch = 0xff
    agio.from_autosteer(wheel_angle, heading, roll, switch, motor_control.pwm_display())
    agio.alive()
    if debug:
        db.write('.')
    time.sleep(0.1)
    if blinker % 32 == 0:
        activity_led.toggle()
        # internal_activity_led.toggle()
    if stop.value() == 0:
        micropython.kbd_intr(3)
        agio.reader.stop=True
        break
    gc.collect()
