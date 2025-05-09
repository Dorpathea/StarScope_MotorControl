#!/usr/bin/python3

# Controlling the Motors using the app with TCP socket
# TCP server

# Required imports
import time
import RPi.GPIO as GPIO
import socket
from subprocess import call

# GPIO pins setup with RPi
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)     # PWMA
GPIO.setup(8, GPIO.OUT)    # AIN2
GPIO.setup(7, GPIO.OUT)    # AIN1
GPIO.setup(12, GPIO.OUT)    # STBY
GPIO.setup(21, GPIO.OUT)     # PWMB
GPIO.setup(20, GPIO.OUT)    # BIN2
GPIO.setup(16, GPIO.OUT)    # BIN1
  
# Turn off Motor A
GPIO.output(25, GPIO.LOW)     # PWMA
GPIO.output(8, GPIO.LOW)    # AIN2
GPIO.output(7, GPIO.LOW)    # AIN1
GPIO.output(12, GPIO.LOW)    # STBY

# Turn off Motor B
GPIO.output(12, GPIO.LOW)    # STBY
GPIO.setup(21, GPIO.LOW)     # PWMB
GPIO.setup(20, GPIO.LOW)    # BIN2
GPIO.setup(16, GPIO.LOW)    # BIN1




GPIO.cleanup()

