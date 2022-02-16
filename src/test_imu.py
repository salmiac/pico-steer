import time
import pico_steer.imu

imu = pico_steer.imu.IMU(True)
while True:
    imu.read()
    time.sleep(0.3)
