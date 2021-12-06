#!/usr/bin/python3

# TCP Client Code

# Import socket module
import socket

# Create socket object
s = socket.socket()

# Define which port you want to connect to
port = 12345

# Connect to the server on the local computer
s.connect(('192.168.1.20', port))       # NEEEEEEEEED TO CHANGE IP ADDRESS HERE TO ACTUAL ONE NEEDED

# Recieve data from the server
#print (s.recv(1024))

data = "Hello"

s.send(data.encode())

# Close the connection
s.close()
