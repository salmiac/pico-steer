from machine import Pin, PWM

pwm0 = None
duty_cycle = 0
direction_pin = Pin(1, Pin.OUT)
pwm0 = PWM(Pin(0))      # create PWM object from a pin
pwm0.freq(25000)        # set frequency
pwm0.duty_u16(duty_cycle)      # set duty cycle, range 0-65535

def start():
    pwm0.duty_u16(duty_cycle)      # set duty cycle, range 0-65535

def stop():
    global duty_cycle
    duty_cycle = 0
    pwm0.duty_u16(0)      # set duty cycle, range 0-65535

def update(value, direction):
    direction_pin.value(direction)
    global duty_cycle
    duty_cycle = int(value / 100.0 * 65535)
    pwm0.duty_u16(duty_cycle)      # set duty cycle, range 0-65535
