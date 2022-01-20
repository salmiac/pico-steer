from machine import Pin
import time

pin = Pin(25, Pin.OUT)

print('Start')
n = 0
while True:
    print('tic', n)
    pin.toggle()
    time.sleep_ms(250)
    n += 1
