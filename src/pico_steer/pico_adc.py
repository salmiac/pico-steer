from machine import ADC, Pin

class Pico_ADC():
    def __init__(self, debug=False):
        Pin(28, Pin.IN)
        self.adc = ADC(Pin(28))
    
    def read(self):
        return self.adc.read_u16() / 2
