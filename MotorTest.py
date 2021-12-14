#!/usr/bin/python3

# Controlling the Motors using the app with TCP socket
# TCP server

# Required imports
import time
import RPi.GPIO as GPIO
import socket
from subprocess import call


def turnBottomMotor():

   # GPIO pins setup with RPi
    #GPIO.setup(12, GPIO.OUT)    # STBY
    #GPIO.setup(21, GPIO.OUT)     # PWMB
    #GPIO.setup(20, GPIO.OUT)    # BIN2
    #GPIO.setup(16, GPIO.OUT)    # BIN1

    # Turn off Motor B
    #GPIO.output(12, GPIO.LOW)    # STBY
    #GPIO.output(21, GPIO.LOW)     # PWMB
    #GPIO.output(20, GPIO.LOW)    # BIN2
    #GPIO.output(16, GPIO.LOW)    # BIN1

    #Clockwise control of Motor B
    #GPIO.output(16, GPIO.HIGH)  # Set BIN1
    #GPIO.output(20, GPIO.LOW)   # Set BIN2
            
    # Set motor speed with PWMB
    #GPIO.output(21, GPIO.HIGH)   # Motor B
            
    #Disable standby with STBY
    #GPIO.output(12, GPIO.HIGH)

    # Slight Delay
    #time.sleep(0.25)

    # Counterclockwise control of Motor B
    GPIO.output(16, GPIO.LOW)  # Set BIN1
    GPIO.output(20, GPIO.HIGH)   # Set BIN2
            
    # Set motor speed with PWMB
    GPIO.output(21, GPIO.HIGH)   # Motor B
            
    #Disable standby with STBY
    GPIO.output(12, GPIO.HIGH)

    # Slight Delay
    time.sleep(0.1)

    # Turn off Motor B
    GPIO.output(12, GPIO.LOW)    # STBY
    GPIO.output(21, GPIO.LOW)     # PWMB
    GPIO.output(20, GPIO.LOW)    # BIN2
    GPIO.output(16, GPIO.LOW)    # BIN1



def turnTopMotor():

    # GPIO pins setup with RPi
    #GPIO.setup(25, GPIO.OUT)     # PWMA
    #GPIO.setup(8, GPIO.OUT)    # AIN2
    #GPIO.setup(7, GPIO.OUT)    # AIN1
    #GPIO.setup(12, GPIO.OUT)    # STBY

    # Turn off Motor A
    GPIO.output(25, GPIO.LOW)     # PWMA
    GPIO.output(8, GPIO.LOW)    # AIN2
    GPIO.output(7, GPIO.LOW)    # AIN1
    GPIO.output(12, GPIO.LOW)    # STBY

   # Clockwise control of Motor A
    #GPIO.output(7, GPIO.HIGH)  # Set AIN1
    #GPIO.output(8, GPIO.LOW)   # Set AIN2
            
    # Set motor speed with PWMA
    #GPIO.output(25, GPIO.HIGH)   # Motor A
            
    #Disable standby with STBY
    #GPIO.output(12, GPIO.HIGH)

    # Slight Delay
    #time.sleep(0.05)

    # Counterclockwise control of Motor A
    GPIO.output(7, GPIO.LOW)  # Set AIN1
    GPIO.output(8, GPIO.HIGH)   # Set AIN2
            
    # Set motor speed with PWMA
    GPIO.output(25, GPIO.HIGH)   # Motor A
            
    #Disable standby with STBY
    GPIO.output(12, GPIO.HIGH)

    # Slight Delay
    time.sleep(0.5)

    # Turn off Motor A
    GPIO.output(25, GPIO.LOW)     # PWMA
    GPIO.output(8, GPIO.LOW)    # AIN2
    GPIO.output(7, GPIO.LOW)    # AIN1
    GPIO.output(12, GPIO.LOW)    # STBY


# GPIO pins setup with RPi
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)     # PWMA
GPIO.setup(8, GPIO.OUT)    # AIN2
GPIO.setup(7, GPIO.OUT)    # AIN1
GPIO.setup(12, GPIO.OUT)    # STBY


#GPIO.output(25, GPIO.LOW)     # PWMA
#GPIO.output(8, GPIO.LOW)    # AIN2
#GPIO.output(7, GPIO.LOW)    # AIN1
#GPIO.output(12, GPIO.LOW)    # STBY
#GPIO.setup(21, GPIO.LOW)     # PWMB
#GPIO.setup(20, GPIO.LOW)    # BIN2
#GPIO.setup(16, GPIO.LOW)    # BIN1

turnTopMotor()

#time.sleep(3)

#GPIO.setup(21, GPIO.OUT)     # PWMB
#GPIO.setup(20, GPIO.OUT)    # BIN2
#GPIO.setup(16, GPIO.OUT)    # BIN1

#turnBottomMotor()

GPIO.cleanup()

# GPIO pins setup with RPi
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(25, GPIO.OUT)     # PWMA
#GPIO.setup(8, GPIO.OUT)    # AIN2
#GPIO.setup(7, GPIO.OUT)    # AIN1
#GPIO.setup(12, GPIO.OUT)    # STBY
#GPIO.setup(21, GPIO.OUT)     # PWMB
#GPIO.setup(20, GPIO.OUT)    # BIN2
#GPIO.setup(16, GPIO.OUT)    # BIN1


# Turn off Motor B
#GPIO.output(12, GPIO.LOW)    # STBY
#GPIO.setup(21, GPIO.LOW)     # PWMB
#GPIO.setup(20, GPIO.LOW)    # BIN2
#GPIO.setup(16, GPIO.LOW)    # BIN1

# Turn off Motor A
#GPIO.output(25, GPIO.LOW)     # PWMA
#GPIO.output(8, GPIO.LOW)    # AIN2
#GPIO.output(7, GPIO.LOW)    # AIN1
#GPIO.output(12, GPIO.LOW)    # STBY

# Clockwise control of Motor A
#GPIO.output(7, GPIO.HIGH)  # Set AIN1
#GPIO.output(8, GPIO.LOW)   # Set AIN2
            
# Set motor speed with PWMA
#GPIO.output(25, GPIO.HIGH)   # Motor A
            
#Disable standby with STBY
#GPIO.output(12, GPIO.HIGH)

# Slight Delay
#time.sleep(3)

# Counterclockwise control of Motor A
#GPIO.output(7, GPIO.LOW)  # Set AIN1
#GPIO.output(8, GPIO.HIGH)   # Set AIN2
            
# Set motor speed with PWMA
#GPIO.output(25, GPIO.HIGH)   # Motor A
            
#Disable standby with STBY
#GPIO.output(12, GPIO.HIGH)

# Slight Delay
#time.sleep(3)

# Turn off Motor A
#GPIO.output(25, GPIO.LOW)     # PWMA
#GPIO.output(8, GPIO.LOW)    # AIN2
#GPIO.output(7, GPIO.LOW)    # AIN1
#GPIO.output(12, GPIO.LOW)    # STBY

#Delay for swapping directions
#time.sleep(3)

#Clockwise control of Motor B
#GPIO.output(16, GPIO.HIGH)  # Set BIN1
#GPIO.output(20, GPIO.LOW)   # Set BIN2
            
# Set motor speed with PWMB
#GPIO.output(21, GPIO.HIGH)   # Motor B
            
#Disable standby with STBY
#GPIO.output(12, GPIO.HIGH)

# Slight Delay
#time.sleep(2)


# Counterclockwise control of Motor B
#GPIO.output(16, GPIO.LOW)  # Set BIN1
#GPIO.output(20, GPIO.HIGH)   # Set BIN2
            
# Set motor speed with PWMB
#GPIO.output(21, GPIO.HIGH)   # Motor B
            
#Disable standby with STBY
#GPIO.output(12, GPIO.HIGH)

# Slight Delay
#time.sleep(2)

# Turn off Motor B
#GPIO.output(12, GPIO.LOW)    # STBY
#GPIO.setup(21, GPIO.LOW)     # PWMB
#GPIO.setup(20, GPIO.LOW)    # BIN2
#GPIO.setup(16, GPIO.LOW)    # BIN1




#GPIO.cleanup()

