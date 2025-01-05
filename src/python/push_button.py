#!/usr/bin/python
# see https://www.youtube.com/watch?v=T67VfwiJPMg

import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM (Broadcom chip-specific pin numbers)
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin number you want to activate (e.g., GPIO 20)
pin_number = 20


def button_callback(channel):
    if GPIO.input(pin_number) == GPIO.HIGH:
        print("released")
    else:
        print("pressed")

GPIO.cleanup()
# Set up the GPIO pin as an intput
GPIO.setup(pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(pin_number, GPIO.BOTH, callback=button_callback, bouncetime=100)

try:
    while True:
        time.sleep(0.05)
except:
    pass

GPIO.cleanup()
