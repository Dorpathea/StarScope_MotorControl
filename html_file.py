#!/usr/bin/env /usr/bin/python3

import cgi
import cgitb
import socket

s = socket.socket()

port = 12345

s.connect(('192.168.1.20', port))

cgitb.enable()

form = cgi.FieldStorage()

searchterm = form.getvalue('Stars')

print("Content-type: text/html\n\n")
print("From your web browser you choose: " + searchterm)

s.send(searchterm.encode())

# Close the connection
s.close()

