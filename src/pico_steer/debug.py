import time
from machine import Pin
from machine import UART, Pin

def now():
    (year, month, mday, hour, minute, second, weekday, yearday) = time.localtime()
    return '{}:{}:{}'.format(hour, minute, second)

_uart = UART(1, baudrate=115200, bits=8, parity=None, stop=1, tx=Pin(8), rx=Pin(9))
_uart.write('Start debugger')

def write(text: str) -> None:
    _uart.write('{} {}\n'.format(now(), text))
