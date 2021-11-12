#!/usr/bin/python3

# Controlling the Motors using the app with TCP socket
# TCP server

# Required imports
import time
import RPi.GPIO as GPIO
import socket
from subprocess import call

def searchKeysByVal(mdict, byval):
    keysList = []
    itemsList = mdict.items()
    for item in itemsList:
        if item[1] == byval:
            keysList.append(item[0])
    return keysList


mydict = {0: "01111111",
          1: "00111111",
          2: "00111110",
          3: "00111010",
          4: "10100011"}


# GPIO pins setup with RPi
GPIO.setmode(GPIO.BCM)

GPIO.setup(27, GPIO.IN)    # 1
GPIO.setup(22, GPIO.IN)    # 2
GPIO.setup(5, GPIO.IN)     # 3
GPIO.setup(6, GPIO.IN)     # 4
GPIO.setup(13, GPIO.IN)    # 5
GPIO.setup(26, GPIO.IN)    # 6
GPIO.setup(23, GPIO.IN)    # 7
GPIO.setup(24, GPIO.IN)    # 8


x=0

#while(1):
while(x<6):
    
    
    a =GPIO.input(24)
    b =GPIO.input(23)
    c =GPIO.input(26)
    d =GPIO.input(13)
    e =GPIO.input(6)
    f =GPIO.input(5)
    g =GPIO.input(22)
    h =GPIO.input(27)


    print(a,b,c,d,e,f,g,h)
#    print(a)
    
    # Convert values to string values and combine them
    aS =str(a)
    bS =str(b)
    cS =str(c)
    dS =str(d)
    eS =str(e)
    fS =str(f)
    gS =str(g)
    hS =str(h)

    Fstring = aS + bS + cS + dS + eS + fS + gS +hS

    #print(Fstring)

    #Fstring = "00111111"

    keysList = searchKeysByVal(mydict, Fstring)

    print(keysList)

    time.sleep(1)

    x+=1

GPIO.cleanup()

