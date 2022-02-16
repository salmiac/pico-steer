import time
import pico_steer.was
import pico_steer.settings

settings = pico_steer.settings.Settings()
was = pico_steer.was.WAS(settings, True)
while True:
    was.read()
    time.sleep(1)
