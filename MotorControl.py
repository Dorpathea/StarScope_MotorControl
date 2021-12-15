#!/usr/bin/python3

# Dorothy Harris and Abby Boucher
# ECE Capstone 2021
# Controlling the Motors and encoders using the webserver application with TCP socket and html

# Required imports
import time
import RPi.GPIO as GPIO
import socket
from subprocess import call
import math
from datetime import datetime


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

# Star names dictionary---> "Name": [RA, DEC]
Snames = {"Aldebaran": [4.6200, 16.5532],
          "Alderamin": [21.3183, 62.6786],
          "Alfirk": [21.4821, 70.6577],
          "Algol": [3.1604, 41.0432],
          "Alpheratz": [0.1590, 29.2131],
          "Altair": [19.8645, 8.9274],
          "Betelgeuse": [5.9396, 7.4106],
          "Capella": [5.3056, 46.0192],
          "Castor": [7.6002, 31.8382],
          "Deneb": [20.7031, 45.3598],
          "Eltanin": [17.9521, 51.4860],
          "Gemma": [15.5938, 26.6401],
          "Hamal": [2.1408, 23.5676],
          "Mira": [2.3412, -1.1229],
          "Mirfak": [3.4320, 49.9393],
          "Polaris": [2.9998, 89.3579],
          "Pollux": [7.7779, 27.9710],
          "Procyon": [7.6744, 5.1675],
          "Rigel": [5.2601, -7.8246],
          "Vega": [18.6281, 38.8047]}


def getMyState(starRA, starDEC, LON, LAT):
    ALT=0.0             # Target altitude
    AZ=0.0              # Target azimuth
    enc_b=0.0           # Desired state of bottom encoder
    enc_t=0.0           # Desired state of top encoder
    secondROT=0.0       # Check if more than one rotation is needed
    tooLow=0.0          # Check if star is below horizon

    # Get target coordinates
    ALT=getALT(starRA, starDEC, LON, LAT)
    AZ=getAZ(starRA, starDEC, LON, LAT, ALT)

    # Convert target coordinates to encoder positions
    # 128 possible positions (0-127), increasing with clockwise rotation
    # Bottom encoder: position 0 faces due north with 1.78 deg between states
    # Top encoder: position 0 faces straight forward with 1.91 deg between states

    # Top encoder
    enc_t=round((ALT/1.91))

    # Bottome encoder is mounted upside-down
    if round((AZ/1.78)) < 128.0:
        enc_b = (128.0 - round((AZ/1.78)))
        secondROT=0.0

    elif round((AZ/1.78)) == 128.0:
        enc_b=0.0
        secondROT=1

    else:
        enc_b=(256.0- round((AZ/1.78)))
        secondROT=1

    # Check if star is below horizon
    if ALT < 0.0:
        tooLow=1

    else:
        tooLow=0.0

    # Return values
    total= [enc_b, enc_t, secondROT, tooLow]
    return total


def getALT(RA_hr, DEC, LON, LAT):
    HA= 0.0
    D= 0.0
    RA= 0.0
    UT= 0.0
    LST= 0.0
    ALT= 0.0
    DS= 0.0

    #Get current time
    hr=datetime.now().hour
    mint=datetime.now().minute
    sec=datetime.now().second
    month=datetime.now().month
    date=datetime.now().day    
    
    # Check for daylight saving
    if month == 3:
            if day >= 17:
                DS=4.0
            else:
                DS=5.0

    elif month >= 4:
        if month < 11:
            DS=4.0

    else:
        DS=5.0



    # Convert right ascension hrs to deg (hrs*15)
    RA=RA_hr*15.0
    
    # Find the time in days from J2000, including the fraction of a day (D)
    D=getD(hr, mint, sec)

    # Find the universal time in decimal hrs
    UT=(hr + ((mint + (sec / 60.0)) / 60.0)) + 5.0

    # Find local sidereal time (LST)
    LST=100.46 + 0.985647 * D + LON + 15.0 * UT

    # Ensure that LST is within 0-360
    while LST < 0.0:
        LST= LST + 360.0

    while LST > 360.0:
        LST= LST - 360.0

    # Calculate hour angle
    HA=LST - RA

    # Ensure HA is within 0-360
    if HA < 0.0:
        HA= HA + 360.0

    elif HA > 360.0:
        HA= HA - 360.0

    # Conver to radians
    HA=HA * math.pi / 180.0
    DEC=DEC * math.pi / 180.0
    LAT=LAT * math.pi / 180.0

    # Calculate altitude
    ALT=math.sin(DEC) * math.sin(LAT) + math.cos(DEC) * math.cos(LAT) * math.cos(HA)
    ALT=math.asin(ALT)

    # Convert back to degrees
    ALT=ALT * 180.0 / math.pi

    print("ALT: ", ALT)
    return ALT


def getAZ(RA_hr, DEC, LON, LAT, ALT):
    A= 0.0
    UT= 0.0
    LST= 0.0
    RA= 0.0
    HA= 0.0
    D= 0.0
    DS= 0.0

    #Get current time
    hr=datetime.now().hour
    mint=datetime.now().minute
    sec=datetime.now().second
    month=datetime.now().month
    date=datetime.now().day    
    
    # Check for daylight saving
    if month == 3:
            if day >= 17:
                DS=4.0
            else:
                DS=5.0

    elif month >= 4:
        if month < 11:
            DS=4.0

    else:
        DS=5.0

    # Convert right ascension hrs to deg (hrs*15)
    RA=RA_hr*15.0
    
    # Find the time in days from J2000, including the fraction of a day (D)
    D=getD(hr, mint, sec)

    # Find the universal time in decimal hrs
    UT=(hr + ((mint + (sec / 60.0)) / 60.0)) + 5.0

    # Find local sidereal time (LST)
    LST=(100.46 + 0.985647 * D + LON + 15.0 * UT)

    # Ensure that LST is within 0-360
    while LST < 0.0:
        LST= LST + 360.0

    while LST > 360.0:
        LST= LST - 360.0

    # Calculate hour angle
    HA=LST - RA

    # Ensure HA is within 0-360
    if HA < 0.0:
        HA= HA + 360.0

    elif HA > 360.0:
        HA= HA - 360.0

    # Convert to radians
    ALT=ALT * math.pi / 180.0
    DEC=DEC * math.pi / 180.0
    LAT=LAT * math.pi / 180.0
    HA=HA * math.pi / 180.0

    # Calculate azimuth
    A= (math.sin(DEC) - math.sin(ALT) * math.sin(LAT)) / (math.cos(ALT) * math.cos(LAT))

    A=math.acos(A)

    # Convert back to degrees
    A=A * 180.0 / math.pi

    if (math.sin(HA)) < 0.0:
        AZ=A

    else:
        AZ= 360.0 - A

    print("AZ: ", AZ)
    return AZ


def getD(hr, mint, sec):
    # D is the time in days from J2000, including the fraction of a day
    D = 0.0
    month2days=0.0
    year=datetime.now().year
    month=datetime.now().month
    date=datetime.now().day

    # Convert years to days
    years2days = (year - 2000.0) * 365.25

    # Convert months to days
    if month == 1:
        month2days = 0.0

    elif month == 2:
        month2days = 31.0

    elif month == 3:
        month2days = 59.0

    elif month == 4:
        month2days = 90.0

    elif month == 5:
        month2days = 120.0

    elif month == 6:
        month2days = 151.0

    elif month == 7:
        month2days = 181.0

    elif month == 8:
        month2days = 211.0

    elif month == 9:
        month2days = 242.0

    elif month == 10:
        month2days = 272.0

    elif month == 11:
        month2days = 303.0

    elif month == 12:
        month2days = 333.0

    # Check if a leap year
    if month > 2:
        if (year % 4) == 0:
            month2days += 1.0

    # Convert time to days
    time2days= (hr + ((mint + (sec / 60.0)) / 60.0)) / 24.0

    D = years2days + month2days + date + time2days
    return D

def turnTopMotor(enc_t):

    # Determine encoders position 
    Encoders= []
    Encoders= encoderValue()

    Current1= Encoders[0]

    print("Enc_t: ", enc_t)

    if enc_t > Current1:
            
        # Clockwise control of Motor A
        GPIO.output(7, GPIO.HIGH)  # Set AIN1
        GPIO.output(8, GPIO.LOW)   # Set AIN2
            
        # Set motor speed with PWMA
        GPIO.output(25, GPIO.HIGH)   # Motor A
            
        #Disable standby with STBY
        GPIO.output(12, GPIO.HIGH)

    elif enc_t < Current1:

        # Counterclockwise control of Motor A
        GPIO.output(7, GPIO.LOW)  # Set AIN1
        GPIO.output(8, GPIO.HIGH)   # Set AIN2
            
        # Set motor speed with PWMA
        GPIO.output(25, GPIO.HIGH)   # Motor A
            
        # Disable standby with STBY
        GPIO.output(12, GPIO.HIGH)

    # Wait until at correct position
    while Current1 != enc_t:
        Encoders= encoderValue()
        Current1= Encoders[0]


    # Turn off Motor A
    GPIO.output(25, GPIO.LOW)     # PWMA
    GPIO.output(8, GPIO.LOW)    # AIN2
    GPIO.output(7, GPIO.LOW)    # AIN1
    GPIO.output(12, GPIO.LOW)    # STBY


def turnBottomMotor(enc_b, SecondROT, secondROT_now):

    # Determine encoders position 
    Encoders= []
    Encoders= encoderValue()

    Current2= Encoders[1]

    print("Enc_b: ", enc_b)
    print("SecondROT_now: ", secondROT_now)
    print("SecondROT: ", SecondROT)
    print("Current2: ", Current2)

    if secondROT_now == SecondROT:

        if enc_b > Current2:

            # Clockwise control of Motor B
            GPIO.output(16, GPIO.HIGH)  # Set BIN1
            GPIO.output(20, GPIO.LOW)   # Set BIN2
            
            # Set motor speed with PWMB
            GPIO.output(21, GPIO.HIGH)  # Motor B
            
            # Disable standby with STBY
            GPIO.output(12, GPIO.HIGH)

            # Wait until at correct position
            while Current2 != enc_b:
                Encoders= encoderValue()
                Current2= Encoders[1]


        elif enc_b < Current2:

            # Counterclockwise control of Motor B
            GPIO.output(16, GPIO.LOW)  # Set BIN1
            GPIO.output(20, GPIO.HIGH)   # Set BIN2
            
            # Set motor speed with PWMB
            GPIO.output(21, GPIO.HIGH)  # Motor B
            
            # Disable standby with STBY
            GPIO.output(12, GPIO.HIGH)

            # Wait until at correct position
            while Current2 != enc_b:
                Encoders= encoderValue()
                Current2= Encoders[1]


    elif secondROT_now > SecondROT:

        # Counterclockwise control of Motor B
        GPIO.output(16, GPIO.LOW)  # Set BIN1
        GPIO.output(20, GPIO.HIGH)   # Set BIN2
            
        # Set motor speed with PWMB
        GPIO.output(21, GPIO.HIGH)  # Motor B
            
        # Disable standby with STBY
        GPIO.output(12, GPIO.HIGH)

        # Overshoot corrent position
        while Current2 != (enc_b-1):
            Encoders= encoderValue()
            Current2= Encoders[1]

        # Wait until at correct position
        while Current2 != enc_b:
            Encoders= encoderValue()
            Current2= Encoders[1]

    elif secondROT_now < SecondROT:

        # Clockwise control of Motor B
        GPIO.output(16, GPIO.HIGH)  # Set BIN1
        GPIO.output(20, GPIO.LOW)   # Set BIN2
            
        # Set motor speed with PWMB
        GPIO.output(21, GPIO.HIGH)  # Motor B
            
        # Disable standby with STBY
        GPIO.output(12, GPIO.HIGH)

        # Overshooot correct position
        while Current2 != (enc_b+1):
            Encoders= encoderValue()
            Current2= Encoders[1]

        # Wait until at correct position
        while Current2 != enc_b:
            Encoders= encoderValue()
            Current2= Encoders[1]

    print("Current2 after: ", Current2)

    # Turn off Motor B
    GPIO.output(12, GPIO.LOW)    # STBY
    GPIO.output(16, GPIO.LOW)    # BIN1
    GPIO.output(20, GPIO.LOW)    # BIN2
    GPIO.output(21, GPIO.LOW)    # PWMB
    
    # Update secondROT_now
    secondROT_now = SecondROT

    return secondROT_now



def encoderValue():

    # ENCODER 
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
    f2 =GPIO.input(18)
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

    values = [Current1, Current2]
    return values


# Set GPIO mode to the GPIO pins (Not the board values)
#GPIO.setmode(GPIO.BCM)

# GPIO pins for Encoder A
#GPIO.setup(27, GPIO.IN)    # 1
#GPIO.setup(22, GPIO.IN)    # 2
#GPIO.setup(5, GPIO.IN)     # 3
#GPIO.setup(6, GPIO.IN)     # 4
#GPIO.setup(13, GPIO.IN)    # 5
#GPIO.setup(26, GPIO.IN)    # 6
#GPIO.setup(23, GPIO.IN)    # 7
#GPIO.setup(24, GPIO.IN)    # 8


# GPIO pins for Encoder B
#GPIO.setup(2, GPIO.IN)      # 1
#GPIO.setup(3, GPIO.IN)      # 2
#GPIO.setup(18, GPIO.IN)      # 3
#GPIO.setup(17, GPIO.IN)     # 4
#GPIO.setup(10, GPIO.IN)     # 5
#GPIO.setup(9, GPIO.IN)      # 6
#GPIO.setup(11, GPIO.IN)     # 7
#GPIO.setup(19, GPIO.IN)     # 8

# Current secondROT flag declaration
secondROT_now = 0.0

# Create the socket object
s = socket.socket()

# Reserve a port
port = 12345

# Bind to the port
s.bind(('', port))

# Put the socket into listening mode
s.listen(5)
# print ("socket is listening")


# A forever loop until we interrupt or an error occurs
while True:

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
    GPIO.setup(18, GPIO.IN)      # 3
    GPIO.setup(17, GPIO.IN)     # 4
    GPIO.setup(10, GPIO.IN)     # 5
    GPIO.setup(9, GPIO.IN)      # 6
    GPIO.setup(11, GPIO.IN)     # 7
    GPIO.setup(19, GPIO.IN)     # 8


    # Establish a connection with the client
    c, addr = s.accept()

    # Try and recieve a message
    data = c.recv(1024)
    result= data.decode()

    # Check if anything was recieved
    if not result: break

    # Error Checking
    print ("Client says: "+ result)

    # MOTOR TURN MATH
    # Get RA and DEC of desired star
    starname= []
    starname= Snames.get(result)

    # Separate parts of array
    RA= starname[0]
    DEC= starname[1]

    # Temporary hard coding lat and lon
    LAT=44.54
    LON=-68.40

    # Return array of desired encoder values
    totalt= []
    totalt= getMyState(RA, DEC, LON, LAT)

    # Separate parts of array
    enc_b= totalt[0]
    enc_t= totalt[1]
    SecondROT= totalt[2]
    tooLow= totalt[3]

    print("TooLow: ", tooLow)

    if tooLow == 1:
        print("Error, star is too low (below horizon)")

    else:

        # GPIO pins setup with RPi for Motor A
        GPIO.setup(25, GPIO.OUT)    # PWMA
        GPIO.setup(8, GPIO.OUT)     # AIN2
        GPIO.setup(7, GPIO.OUT)     # AIN1
        GPIO.setup(12, GPIO.OUT)    # STBY

        turnTopMotor(enc_t)

        time.sleep(3)

        # GPIO pins setup with RPi for Motor B
        GPIO.setup(16, GPIO.OUT)    # BIN1
        GPIO.setup(20, GPIO.OUT)    # BIN2
        GPIO.setup(21, GPIO.OUT)    # PWMB

        secondROT_now= turnBottomMotor(enc_b, SecondROT, secondROT_now)

    # Release GPIO pins
    GPIO.cleanup()

    # Close the connection with the client
    c.close()
   
# Make sure everything is off
c.close()
GPIO.cleanup()


