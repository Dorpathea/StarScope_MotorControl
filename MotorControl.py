#!/usr/bin/python3

# Required imports
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

# GPIO pins setup with RPi
GPIO.setup(7, GPIO.OUT)     # PWMA
GPIO.setup(11, GPIO.OUT)    # AIN2
GPIO.setup(12, GPIO.OUT)    # AIN1
GPIO.setup(13, GPIO.OUT)    # STBY
GPIO.setup(15, GPIO.OUT)    # BIN1
GPIO.setup(16, GPIO.OUT)    # BIN2
GPIO.setup(18, GPIO.OUT)    # PWMB

#For clockwise control

# Motor A
GPIO.output(12, GPIO.HIGH)  # Set AIN1
GPIO.output(11, GPIO.LOW)   # Set AIN2

# Motor B
GPIO.output(15, GPIO.HIGH)  # Set BIN1
GPIO.output(16, GPIO.LOW)   # Set BIN2

# Set motor speed with PWMA and PWMB
GPIO.output(7, GPIO.HIGH)   # Motor A
GPIO.output(18, GPIO.HIGH)  # Motor B

#Disable standby with STBY
GPIO.output(13, GPIO.HIGH)

# Wait
time.sleep(3)

#For counterclockwise control

# Motor A
GPIO.output(12, GPIO.LOW)  # Set AIN1
GPIO.output(11, GPIO.HIGH)   # Set AIN2

# Motor B
GPIO.output(15, GPIO.LOW)  # Set BIN1
GPIO.output(16, GPIO.HIGH)   # Set BIN2
# Set motor speed with PWMA and PWMB
GPIO.output(7, GPIO.HIGH)   # Motor A
GPIO.output(18, GPIO.HIGH)  # Motor B

#Disable standby with STBY
GPIO.output(13, GPIO.HIGH)

# Wait
time.sleep(3)

# Reset all GPIO pins

GPIO.output(7, GPIO.LOW)     # PWMA
GPIO.output(11, GPIO.LOW)    # AIN2
GPIO.output(12, GPIO.LOW)    # AIN1
GPIO.output(13, GPIO.LOW)    # STBY
GPIO.output(15, GPIO.LOW)    # BIN1
GPIO.output(16, GPIO.LOW)    # BIN2
GPIO.output(18, GPIO.LOW)    # PWMB

