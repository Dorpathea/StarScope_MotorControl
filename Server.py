#!/usr/bin/python3

# Controlling the Motors using the app with TCP socket
# TCP server

# Required imports
import socket
import time
import RPi.GPIO as GPIO
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
    #Get current time
    hr=datetime.now().hour
    mint=datetime.now().minute
    sec=datetime.now().second

    # Convert right ascension hrs to deg (hrs*15)
    RA=RA_hr*15.0
    
    # Find the time in days from J2000, including the fraction of a day (D)
    D=getD(hr, mint, sec)

    # Find the universal time in decimal hrs
    UT=(hr + ((mint + (sec / 60.0)) / 60.0)) + 4.0

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
    HA=HA * 3.14159 / 180.0
    DEC=DEC * 3.14159 / 180.0
    LAT=LAT * 3.14159 / 180.0

    # Calculate altitude
    ALT=math.sin(DEC) * math.sin(LAT) + math.cos(DEC) * math.cos(LAT) * math.cos(HA)
    ALT=math.asin(ALT)

    # Convert back to degrees
    ALT=ALT * 180.0 / 3.14159

    return ALT

def getAZ(RA_hr, DEC, LON, LAT, ALT):
    #Get current time
    hr=datetime.now().hour
    mint=datetime.now().minute
    sec=datetime.now().second

    # Convert right ascension hrs to deg (hrs*15)
    RA=RA_hr*15.0
    
    # Find the time in days from J2000, including the fraction of a day (D)
    D=getD(hr, mint, sec)

    # Find the universal time in decimal hrs
    UT=(hr + ((mint + (sec / 60.0)) / 60.0)) + 4.0

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

    # Convert to radians
    ALT=ALT * 3.14159 / 180.0
    DEC=DEC * 3.14159 / 180.0
    LAT=LAT * 3.14159 / 180.0

    # Calculate azimuth
    A= (math.sin(DEC) - math.sin(ALT) * math.sin(LAT)) / (math.cos(ALT) * math.cos(LAT))

    # Convert back to degrees
    A=A * 180.0 / 3.14159

    if (math.sin(HA)) < 0.0:
        AZ=A

    else: 
        AZ= 360.0 - A

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
    if month >= 1:
        month2days = 0.0

    if month >= 2:
        month2days = 31.0

    # Check if leap year
    if month >= 3:
        if (year % 4) == 0:
            month2days += 29.0
        else:
            month2days +=28.0

        if month >= 4:
            month2days += 31.0

            if month >= 5:
                month2days += 30.0

                if month >= 6:
                    month2days += 31.0

                    if month >= 7:
                        month2days += 30.0

                        if month >= 8:
                            month2days += 30.0

                            if month >= 9:
                                month2days += 31.0

                                if month >= 10:
                                    month2days += 30.0

                                    if month >= 11:
                                        month2days += 31.0

                                        if month >= 12:
                                            month2days += 30.0

    # Convert time to days
    time2days= (hr + ((mint + (sec / 60.0)) / 60.0)) * 24.0

    D = years2days + month2days + date + time2days
    return D


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
    data = c.recv(1024)
    result= data.decode()

    # Check if anything was recieved
    if not result: break

    # Error Checking
    print ("Client says: " + result)

    starName= []
    starName = Snames.get(result)

    # Seperate parts
    RA = starName[0]
    DEC = starName[1]

    # Temporary hard coding lat and lon
    LAT=44.9
    LON=-68.7

    # Return array
    totalt= []
    totalt = getMyState(RA, DEC, LON, LAT)

    # Seperate parts
    enc_b=totalt[0]
    enc_t=totalt[1]
    secondROT=totalt[2]
    tooLow=totalt[3]

    print("TooLow")
    print(tooLow)

    if tooLow == 1:
        print("error, star too low (below horizon)")

    else:
        print("yay")
        print(enc_b)
        print(enc_t)
        print(secondROT)

     #   print("Error here")
        # Tell app message was recieved
        #conn.sendall("Server Says: Recieved")
        # Splits two recieved numbers into seperate strings
    # Close the connection with the client
    c.close()

c.close()


