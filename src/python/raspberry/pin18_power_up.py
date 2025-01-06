#!/usr/bin/python

import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM (Broadcom chip-specific pin numbers)
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin number you want to activate (e.g., GPIO 18)
pin_number = 18

# Set up the GPIO pin as an output
GPIO.setup(pin_number, GPIO.OUT)

try:
    # Activate the pin (set it high)
    GPIO.output(pin_number, GPIO.HIGH)
    print(f"GPIO {pin_number} is now HIGH.")

    # Keep it high for 5 seconds
    time.sleep(5)

finally:
    # Deactivate the pin (set it low)
    GPIO.output(pin_number, GPIO.LOW)
    print(f"GPIO {pin_number} is now LOW.")

    # Clean up the GPIO settings
    GPIO.cleanup()
