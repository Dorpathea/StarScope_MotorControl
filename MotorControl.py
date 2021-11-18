#!/usr/bin/python3

# Dorothy Harris and Abby Boucher
# ECE Capstone 2021
# Controlling the Motors and encoders using the app with TCP socket (Server)

# Required imports
import time
import RPi.GPIO as GPIO
import socket
from subprocess import call

# Function for looking through the dictionary
def searchKeysByVal(mdict, byval):
    keysList = []
    itemsList = mdict.items()
    for item in itemsList:
        if item[1] == byval:
            keysList.append(item[0])
    return keysList

# Dictionary of Encoder values to look up from later
mydict = {0: "01111111",
          1: "00111111",
          2: "00111110",
          3: "00111010",
          4: "00111000",
          5: "10111000",
          6: "10011000",
          7: "00011000",
          8: "00001000",
          9: "01001000",
          10: "01001001",
          11: "01001101",
          12: "01001111",
          13: "00001111",
          14: "00101111",
          15: "10101111",
          16: "10111111",
          17: "10011111",
          18: "00011111",
          19: "00011101",
          20: "00011100",
          21: "01011100",
          22: "01001100",
          23: "00001100",
          24: "00000100",
          25: "00100100",
          26: "10100100",
          27: "10100110",
          28: "10100111",
          29: "10000111",
          30: "10010111",
          31: "11010111",
          32: "11011111",
          33: "11001111",
          34: "10001111",
          35: "10001110",
          36: "00001110",
          37: "00101110",
          38: "00100110",
          39: "00000110",
          40: "00000010",
          41: "00010010",
          42: "01010010",
          43: "01010011",
          44: "11010011",
          45: "11000011",
          46: "11001011",
          47: "11101011",
          48: "11101111",
          49: "11100111",
          50: "11000111",
          51: "01000111",
          52: "00000111",
          53: "00010111",
          54: "00010011",
          55: "00000011",
          56: "00000001",
          57: "00001001",
          58: "00101001",
          59: "10101001",
          60: "11101001",
          61: "11100001",
          62: "11100101",
          63: "11110101",
          64: "11110111",
          65: "11110011",
          66: "11100011",
          67: "10100011",
          68: "10000011",
          69: "10001011",
          70: "10001001",
          71: "10000001",
          72: "10000000",
          73: "10000100",
          74: "10010100",
          75: "11010100",
          76: "11110100",
          77: "11110000",
          78: "11110010",
          79: "11111010",
          80: "11111011",
          81: "11111001",
          82: "11110001",
          83: "11010001",
          84: "11000001",
          85: "11000101",
          86: "11000100",
          87: "11000000",
          88: "01000000",
          89: "01000010",
          90: "01001010",
          91: "01101010",
          92: "01111010",
          93: "01111000",
          94: "01111001",
          95: "01111101",
          96: "11111101",
          97: "11111100",
          98: "11111000",
          99: "11101000",
          100: "11100000",
          101: "11100010",
          102: "01100010",
          103: "01100000",
          104: "00100000",
          105: "00100001",
          106: "00100101",
          107: "00110101",
          108: "00111101",
          109: "00111100",
          110: "10111100",
          111: "10111110",
          112: "11111110",
          113: "01111110",
          114: "01111100", 
          115: "01110100",
          116: "01110000",
          117: "01110001",
          118: "00110001",
          119: "00110000",
          120: "00010000",
          121: "10010000",
          122: "10010010",
          123: "10011010",
          124: "10011110",
          125: "00011110",
          126: "01011110",
          127: "01011111"}


# Set GPIO mode to the GPIO pins (Not the board values)
GPIO.setmode(GPIO.BCM)

# GPIO pins for Encoder A
GPIO.setup(27, GPIO.IN)    # 1
GPIO.setup(22, GPIO.IN)    # 2
GPIO.setup(5, GPIO.IN)     # 3
GPIO.setup(6, GPIO.IN)     # 4
GPIO.setup(13, GPIO.IN)    # 5
GPIO.setup(26, GPIO.IN)    # 6
GPIO.setup(23, GPIO.IN)    # 7
GPIO.setup(24, GPIO.IN)    # 8


# GPIO pins for Encoder B
GPIO.setup(2, GPIO.IN)      # 1
GPIO.setup(3, GPIO.IN)      # 2
GPIO.setup(4, GPIO.IN)      # 3
GPIO.setup(17, GPIO.IN)     # 4
GPIO.setup(10, GPIO.IN)     # 5
GPIO.setup(9, GPIO.IN)      # 6
GPIO.setup(11, GPIO.IN)     # 7
GPIO.setup(19, GPIO.IN)     # 8


# GPIO pins setup with RPi (WILL NEED TO BE CHANGED!)
GPIO.setup(25, GPIO.OUT)    # PWMA
GPIO.setup(8, GPIO.OUT)     # AIN2
GPIO.setup(7, GPIO.OUT)     # AIN1
GPIO.setup(12, GPIO.OUT)    # STBY
GPIO.setup(16, GPIO.OUT)    # BIN1
GPIO.setup(20, GPIO.OUT)    # BIN2
GPIO.setup(21, GPIO.OUT)    # PWMB

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
    c, addr = s.accept()
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
        state = int(datalist[2])

        # Finding current state of Encoder A
        a =GPIO.input(24)
        b =GPIO.input(23)
        c =GPIO.input(26)
        d =GPIO.input(13)
        e =GPIO.input(6)
        f =GPIO.input(5)
        g =GPIO.input(22)
        h =GPIO.input(27)

        # Finding current state of Encoder B
        a2 =GPIO.input(19)
        b2 =GPIO.input(11)
        c2 =GPIO.input(9)
        d2 =GPIO.input(10)
        e2 =GPIO.input(17)
        f2 =GPIO.input(4)
        g2 =GPIO.input(3)
        h2 =GPIO.input(2)

        # Convert values to string values and combine them for Encoder A
        aS =str(a)
        bS =str(b)
        cS =str(c)
        dS =str(d)
        eS =str(e)
        fS =str(f)
        gS =str(g)
        hS =str(h)
        Fstring = aS + bS + cS + dS + eS + fS + gS +hS

        # Convert values to string values and combine them for Encoder B
        a2S =str(a2)
        b2S =str(b2)
        c2S =str(c2)
        d2S =str(d2)
        e2S =str(e2)
        f2S =str(f2)
        g2S =str(g2)
        h2S =str(h2)
        Fstring2 = a2S + b2S + c2S + d2S + e2S + f2S + g2S +h2S


        # Search dictionary for what state it's currently in for the Encoder
        Encoder1 = searchKeysByVal(mydict, Fstring)
        Encoder2 = searchKeysByVal(mydict, Fstring2)

        # Change into an int for comparison
        Current1 = Encoder1[0]
        Current2 = Encoder2[0]


        if motor1 < Current1:
            
            # Clockwise control of Motor A
            GPIO.output(7, GPIO.HIGH)  # Set AIN1
            GPIO.output(8, GPIO.LOW)   # Set AIN2
            
            # Set motor speed with PWMA
            GPIO.output(25, GPIO.HIGH)   # Motor A
            
            #Disable standby with STBY
            GPIO.output(12, GPIO.HIGH)

        elif motor1 > Current1:

            # Counterclockwise control of Motor A
            GPIO.output(7, GPIO.LOW)  # Set AIN1
            GPIO.output(8, GPIO.HIGH)   # Set AIN2
            
            # Set motor speed with PWMA
            GPIO.output(25, GPIO.HIGH)   # Motor A
            
            #Disable standby with STBY
            GPIO.output(12, GPIO.HIGH)

        # Wait until at correct position
        while motor1 != Current1:

        # Turn off Motor A
        GPIO.output(25, GPIO.LOW)     # PWMA
        GPIO.output(8, GPIO.LOW)    # AIN2
        GPIO.output(7, GPIO.LOW)    # AIN1
        GPIO.output(12, GPIO.LOW)    # STBY


        if motor2 < Current2:

            # Clockwise control of Motor B
            GPIO.output(16, GPIO.HIGH)  # Set BIN1
            GPIO.output(20, GPIO.LOW)   # Set BIN2
            
            # Set motor speed with PWMB
            GPIO.output(21, GPIO.HIGH)  # Motor B
            
            #Disable standby with STBY
            GPIO.output(12, GPIO.HIGH)


        elif motor2 > Current2:

            # Counterclockwise control of Motor B
            GPIO.output(16, GPIO.LOW)  # Set BIN1
            GPIO.output(20, GPIO.HIGH)   # Set BIN2
            
            # Set motor speed with PWMB
            GPIO.output(21, GPIO.HIGH)  # Motor B
            
            #Disable standby with STBY
            GPIO.output(12, GPIO.HIGH)

        # Wait until at correct position
        while motor2 != Current2:

        # Turn off Motor B
        GPIO.output(12, GPIO.LOW)    # STBY
        GPIO.output(16, GPIO.LOW)    # BIN1
        GPIO.output(20, GPIO.LOW)    # BIN2
        GPIO.output(21, GPIO.LOW)    # PWMB


    except socket.error:
        print "Error Occured."
        break

# Close the connection with the client
c.close()

# WILL NEED TO BE CHANGED AND ADDED TO
# Reset all GPIO pins
# Make sure everything has stopped moving
# Not sure if needed
GPIO.output(25, GPIO.LOW)     # PWMA
GPIO.output(8, GPIO.LOW)    # AIN2
GPIO.output(7, GPIO.LOW)    # AIN1
GPIO.output(12, GPIO.LOW)    # STBY
GPIO.output(16, GPIO.LOW)    # BIN1
GPIO.output(20, GPIO.LOW)    # BIN2
GPIO.output(21, GPIO.LOW)    # PWMB

# Release GPIO pins
GPIO.cleanup()

# Shutdown Pi
#call("sudo nohup shutdown -h now", shell=True)


