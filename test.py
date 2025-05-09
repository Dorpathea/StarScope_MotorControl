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


# GPIO pins setup with RPi
GPIO.setmode(GPIO.BCM)

# Encoder A
GPIO.setup(27, GPIO.IN)    # 1
GPIO.setup(22, GPIO.IN)    # 2
GPIO.setup(5, GPIO.IN)     # 3
GPIO.setup(6, GPIO.IN)     # 4
GPIO.setup(13, GPIO.IN)    # 5
GPIO.setup(26, GPIO.IN)    # 6
GPIO.setup(23, GPIO.IN)    # 7
GPIO.setup(24, GPIO.IN)    # 8


# Encoder B
GPIO.setup(2, GPIO.IN)      # 1
GPIO.setup(3, GPIO.IN)      # 2
GPIO.setup(4, GPIO.IN)      # 3
GPIO.setup(17, GPIO.IN)     # 4
GPIO.setup(10, GPIO.IN)     # 5
GPIO.setup(9, GPIO.IN)      # 6
GPIO.setup(11, GPIO.IN)     # 7
GPIO.setup(19, GPIO.IN)     # 8




#x=0

#while(1):
while True:
    
    # Setting to input values
    a =GPIO.input(24)
    b =GPIO.input(23)
    c =GPIO.input(26)
    d =GPIO.input(13)
    e =GPIO.input(6)
    f =GPIO.input(5)
    g =GPIO.input(22)
    h =GPIO.input(27)

    a2 =GPIO.input(19)
    b2 =GPIO.input(11)
    c2 =GPIO.input(9)
    d2 =GPIO.input(10)
    e2 =GPIO.input(17)
    f2 =GPIO.input(4)
    g2 =GPIO.input(3)
    h2 =GPIO.input(2)

    #print(a,b,c,d,e,f,g,h)

    #print(a2,b2,c2,d2,e2,f2,g2,h2)

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

    a2S =str(a2)
    b2S =str(b2)
    c2S =str(c2)
    d2S =str(d2)
    e2S =str(e2)
    f2S =str(f2)
    g2S =str(g2)
    h2S =str(h2)

    Fstring = aS + bS + cS + dS + eS + fS + gS +hS

    Fstring2 = a2S + b2S + c2S + d2S + e2S + f2S + g2S +h2S

    print("Binary of Encoder1:", Fstring)

    print("Binary of Encoder2:", Fstring2)

    Encoder1 = searchKeysByVal(mydict, Fstring)
    Current1 = Encoder1[0]
    print("Encoder1 value", Current1)

    Encoder2 = searchKeysByVal(mydict, Fstring2)
    Current2 = Encoder2[0]
    print("Encoder2 value", Current2)

    print(" ")


 #   intit = keysList[0]

 #   if (intit == 0):
  #      print("yes")

    time.sleep(1)

   # x+=1

GPIO.cleanup()

