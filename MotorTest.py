#!/usr/bin/python3

# Controlling the Motors using the app with TCP socket
# TCP server

# Required imports
import time
import RPi.GPIO as GPIO
import socket
from subprocess import call

# GPIO pins setup with RPi
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)     # PWMA
GPIO.setup(11, GPIO.OUT)    # AIN2
GPIO.setup(12, GPIO.OUT)    # AIN1
GPIO.setup(13, GPIO.OUT)    # STBY
    

# Clockwise control of Motor A
GPIO.output(12, GPIO.HIGH)  # Set AIN1
GPIO.output(11, GPIO.LOW)   # Set AIN2
            
# Set motor speed with PWMA
GPIO.output(7, GPIO.HIGH)   # Motor A
            
#Disable standby with STBY
GPIO.output(13, GPIO.HIGH)


time.sleep(5)

# Turn off Motor A
GPIO.output(7, GPIO.LOW)     # PWMA
GPIO.output(11, GPIO.LOW)    # AIN2
GPIO.output(12, GPIO.LOW)    # AIN1
GPIO.output(13, GPIO.LOW)    # STBY

# Counterclockwise control of Motor A
GPIO.output(12, GPIO.LOW)  # Set AIN1
GPIO.output(11, GPIO.HIGH)   # Set AIN2
            
# Set motor speed with PWMA
GPIO.output(7, GPIO.HIGH)   # Motor A
            
#Disable standby with STBY
GPIO.output(13, GPIO.HIGH)

time.sleep(5)



# Reset all GPIO pins
# Make sure everything has stopped moving
# Not sure if needed
GPIO.output(7, GPIO.LOW)     # PWMA
GPIO.output(11, GPIO.LOW)    # AIN2
GPIO.output(12, GPIO.LOW)    # AIN1
GPIO.output(13, GPIO.LOW)    # STBY

GPIO.cleanup()

