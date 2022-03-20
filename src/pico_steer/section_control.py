from machine import Pin
import time

DELAY = 5

relays = []
relay_pins = [19, 20, 21, 22, 26, 27, 6, 7, 10, 11]
for n in range(10):
    relay = Pin(relay_pins[n], Pin.OUT)
    relay.off()
    relays.append(relay)
up_down_mode = Pin(18, Pin.IN, Pin.PULL_UP)

def _section_status(sc, n) -> int:
    return 1 if (1 << n & sc) else 0

class SectionControl():
    def __init__(self) -> None:
        self.up_down_status = 0
        self.up_down_time = 0

    def up_down(self, status) -> None:
        if status != self.up_down_status:
            self.up_down_status = status
            if status:
                relays[8].on()
                relays[9].off()
            else:
                relays[9].on()
                relays[8].off()
            self.up_down_time = time.time()
            return

        if self.up_down_time + DELAY < time.time():
            relays[8].off()
            relays[9].off()

    def update(self, sc) -> None:
        if up_down_mode.value() == 0:
            self.up_down(_section_status(sc, 0))
            return
        
        for n in range(10):
            relays[n].value(_section_status(sc, n))
