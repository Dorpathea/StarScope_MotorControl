#!/usr/bin/python3

# Controlling the Motors using the app with TCP socket
# TCP server

# Required imports
import socket

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
        print ("Client says: "+data)
    except:
        print("Error")
        # Tell app message was recieved
        #conn.sendall("Server Says: Recieved")
        # Splits two recieved numbers into seperate strings
    # Close the connection with the client
    c.close()

