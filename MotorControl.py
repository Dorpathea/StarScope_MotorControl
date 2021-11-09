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
GPIO.setup(15, GPIO.OUT)    # BIN1
GPIO.setup(16, GPIO.OUT)    # BIN2
GPIO.setup(18, GPIO.OUT)    # PWMB

# Create the socket object
s = socket.socket()
# print ("Socket successfully created")

# Reserve a port
port = 12345

# Bind to the port
s.bind(('', port))

# Put the socket into listening mode
s.listen(5)
# print ("socket is listening")

# A forever loop until we interrupt or an error occurs
while True:

    # Establish a connection with the client
    c, addr = s.accept
    # print ('Got connection from', addr)

    # Send a thank you message to client
    # c.send('Thank you for connecting')

    # Try and recieve a message
    try:
        data = c.recv(1024)

        # Check if anything was recieved
        if not data: break

        # Error Checking
        print "Client says: "+data

        # Tell app message was recieved
        conn.sendall("Server Says: Recieved")


        # Splits two recieved numbers into seperate strings
        datalist = data.split()
        
        # Convert strings to integers
        motor1 = int(datalist[0])
        motor2 = int(datalist[1])

    
        if motor1 < Current1:
            
            # Clockwise control of Motor A
            GPIO.output(12, GPIO.HIGH)  # Set AIN1
            GPIO.output(11, GPIO.LOW)   # Set AIN2
            
            # Set motor speed with PWMA
            GPIO.output(7, GPIO.HIGH)   # Motor A
            
            #Disable standby with STBY
            GPIO.output(13, GPIO.HIGH)

        elif motor1 > Current1:

            # Counterclockwise control of Motor A
            GPIO.output(12, GPIO.LOW)  # Set AIN1
            GPIO.output(11, GPIO.HIGH)   # Set AIN2
            
            # Set motor speed with PWMA
            GPIO.output(7, GPIO.HIGH)   # Motor A
            
            #Disable standby with STBY
            GPIO.output(13, GPIO.HIGH)

        # Wait until at correct position
        while motor1 != Current1:

        # Turn off Motor A
        GPIO.output(7, GPIO.LOW)     # PWMA
        GPIO.output(11, GPIO.LOW)    # AIN2
        GPIO.output(12, GPIO.LOW)    # AIN1
        GPIO.output(13, GPIO.LOW)    # STBY


        if motor2 < Current2:

            # Clockwise control of Motor B
            GPIO.output(15, GPIO.HIGH)  # Set BIN1
            GPIO.output(16, GPIO.LOW)   # Set BIN2
            
            # Set motor speed with PWMB
            GPIO.output(18, GPIO.HIGH)  # Motor B
            
            #Disable standby with STBY
            GPIO.output(13, GPIO.HIGH)


        elif motor2 > Current2:

            # Counterclockwise control of Motor B
            GPIO.output(15, GPIO.LOW)  # Set BIN1
            GPIO.output(16, GPIO.HIGH)   # Set BIN2
            
            # Set motor speed with PWMB
            GPIO.output(18, GPIO.HIGH)  # Motor B
            
            #Disable standby with STBY
            GPIO.output(13, GPIO.HIGH)

        # Wait until at correct position
        while motor2 != Current2:

        # Turn off Motor B
        GPIO.output(13, GPIO.LOW)    # STBY
        GPIO.output(15, GPIO.LOW)    # BIN1
        GPIO.output(16, GPIO.LOW)    # BIN2
        GPIO.output(18, GPIO.LOW)    # PWMB


    except socket.error:
        print "Error Occured."
        break

# Close the connection with the client
c.close()

# Reset all GPIO pins
# Make sure everything has stopped moving
# Not sure if needed
GPIO.output(7, GPIO.LOW)     # PWMA
GPIO.output(11, GPIO.LOW)    # AIN2
GPIO.output(12, GPIO.LOW)    # AIN1
GPIO.output(13, GPIO.LOW)    # STBY
GPIO.output(15, GPIO.LOW)    # BIN1
GPIO.output(16, GPIO.LOW)    # BIN2
GPIO.output(18, GPIO.LOW)    # PWMB

# Shutdown Pi
#call("sudo nohup shutdown -h now", shell=True)

