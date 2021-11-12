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

GPIO.setup(17, GPIO.IN)    # C
GPIO.setup(27, GPIO.IN)    # 1
GPIO.setup(22, GPIO.IN)    # 2
GPIO.setup(5, GPIO.IN)     # 3
GPIO.setup(6, GPIO.IN)     # 4
GPIO.setup(13, GPIO.IN)    # 5
GPIO.setup(26, GPIO.IN)    # 6
GPIO.setup(23, GPIO.IN)    # 7
GPIO.setup(24, GPIO.IN)    # 8

while(1):
    a =GPIO.input(24)
#    b =GPIO.input(23)
#    c =GPIO.input(26)
#    d =GPIO.input(13)
#    e =GPIO.input(6)
#    f =GPIO.input(5)
#    g =GPIO.input(22)
#    h =GPIO.input(27)


#    print(a,b,c,d,e,f,g,h)
    print(a)

    time.sleep(1)

