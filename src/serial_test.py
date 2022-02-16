import time
from machine import UART, Pin

uart = UART(1, baudrate=115200, bits=8, parity=None, stop=1, tx=Pin(8), rx=Pin(9))

internal_activity_led = Pin(25, Pin.OUT)

while True:
    for n in range(255):
        internal_activity_led.toggle()
        uart.write('Number: {:X}'.format(n))
        print(uart.read())
        time.sleep(0.1)
    