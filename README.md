# pico-steer
Raspberry Pi Pico based autosteer software

## Notice!
I left this 'as is'. I gave up on developing this. Indivual parts should work. There are probably some problems. The main reason to give up is Windows USB - serial port. One USB - serial GPS works well. Add Raspberry Pi Pico USB - serial to it with USB hub and serial ports stop working.
I continue using Raspberry Pi 3 https://github.com/salmiac/pi-steer

## Warning
This just just for demonstration and proof of concept. This should never ever be used on full sized machinery. You will crash and die if You do. You have been warned.

## Rapberry Pi Pico

Techincal specification https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html#technical-specification

How to get 5V power output from Raspberry pi Pico https://raspberrypi.stackexchange.com/questions/127864/how-to-get-5v-power-output-from-raspberry-pi-pico

### Micropython

MicroPython for Pico and RP2 Resources https://forums.raspberrypi.com/viewtopic.php?t=310062

Documentation https://docs.micropython.org/en/latest/rp2/quickref.html

Latest Micropython firmware https://micropython.org/download/rp2-pico/rp2-pico-latest.uf2

Raspberry Pi Pico and Mincropython on Windows https://picockpit.com/raspberry-pi/raspberry-pi-pico-and-micropython-on-windows/

Pico-Go VS Code Extension http://pico-go.net/

Resetting Pico Flash memory https://datasheets.raspberrypi.com/soft/flash_nuke.uf2

### Adafruit CircuitPython

https://circuitpython.org/board/raspberry_pi_pico/

Getting Started with Raspberry Pi Pico and CircuitPython https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython

## Hardware

### Raspberry Pi Pico pin connections

|Device|pin|number|number|pin|Device|
|--|--|--|--|--|--|
|PWM|GP0|1|40|VBUS|BSS138 HV, DC VDD|
|PWM direction|GP1|2|39|VSYS||
|BSS138, ADC GND|GND|3|38|GND|BSS138 GND|
|BSS138, ADC I2C SDA|I2C1 SDA/GP2|4|37|3V3_EN||
|BSS138, ADC I2C SCL|I2C1 SCL/GP3|5|36|3V3(OUT)|BSS138 LV, IMU Vin, LED +|
|IMU I2C SDA|I2C0 SDA/GP4|6|35|ADC_VREF|WAS 5V|
|IMU I2C SCL|I2C0 SCL/GP5|7|34|GP28|WAS signal|
|IMU GND|GND|8|33|GND|WAS GND|
|relay 6|GP6|9|32|GP27|relay 5|
|relay 7|GP7|10|31|GP26|relay 4|
|debug serial TX|GP8|11|30|RUN||
|debug serial RX|GP9|12|29|GP22|relay 3|
|PWM GND|GND|13|28|GND|Power on LED -|
|relay 8|GP10|14|27|GP21|relay 2, section 3|
|relay 9|GP11|15|26|GP20|relay 1, section 2|
|Work switch|GP12|16|25|GP19|relay 0, section 1|
|Autosteer switch|GP13|17|24|GP18|Optional mode select jumper or switch|
|Autosteer switch|GND|18|23|GND|Optional mode select jumper GND|
|Motor direction LED -|GP14|19|22|GP17|Activity LED -|
|Stop the program|GP15|20|21|GP16|Autosteer activated LED -|

### Inertial masurement unit (IMU)
Connected via I2C 

https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles

#### BNO055 

https://github.com/adafruit/Adafruit_BNO055

https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bno055-ds000.pdf

#### BNO085


### Wheel angle sensor (WAS)
Pico board has it self an analog to digital converter (ADC) that could be used. However **RTY120LVNAA** https://sps.honeywell.com/us/en/products/sensing-and-iot/sensors/motion-and-position-sensors/magnetic-position-sensors/rty-series that is used here is rated for 5 V (output 0.5 V to 4.5 V) and Pico ADC is for 3.3 V Therefor internal ADC can't be used. Instead external ADC is used. Here it is Adafruit 16 bit ADC **ADS1115** http://adafru.it/1085 datasheet https://cdn-shop.adafruit.com/datasheets/ads1115.pdf . Yet another external board is needed for 3.3 V - 5 V conversion Adafruit 4-channel I2C-safe Bi-directional logic level converter **BSS138** http://adafru.it/757.

|Pico|Pico number|BSS138 LV|BSS138 HV|ADS1115|RTY120LVNAA|RTY pin|
|--|--|--|--|--|--|--|
|3v3 Power|36|LV|||||
|VBUS|40||HV|VDD|Vcc 5V|1/A|
|GND|38|GND|GND|GND|GND|2/B|
|I2C1 SCL/GP2|5|A1|B1|SCL|||
|I2C1 SDA/GP2|4|A2|B2|SDA|||
|||||A0|output|3/C|

The other possibility is to use voltage divider with two resistors e.g. 330k and 180k. 180k between output and ADC0 and 330k between GND and ADC0. 

|Pico|Pico number|RTY120LVNAA|RTY pin|
|--|--|--|--|
|VBUS|40|Vcc 5V|1/A|
|GND|38|GND|2/B|
|GP26/ADC0|31|output|3/C|
