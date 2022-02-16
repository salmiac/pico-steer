import pico_steer.agio
import pico_steer.settings
import pico_steer.motor_control
import time
from machine import Pin
import micropython
import gc

stop = Pin(15, Pin.IN, Pin.PULL_UP)

settings = pico_steer.settings.Settings()
motor_control = pico_steer.motor_control.MotorControl(settings)

agio = pico_steer.agio.AgIO(settings, motor_control, False)
agio.start_reader()

while True:
    if stop.value() == 0:
        print('Stop')
        micropython.kbd_intr(3)
        agio.reader.stop = True
        break
    agio.alive()
    # print('Mem:', gc.mem_alloc(), gc.mem_free())
    gc.collect()
    time.sleep(0.1)












