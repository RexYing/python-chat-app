'''
Created on Dec 3, 2013

@author: yzt
'''

import socket               # Import socket module

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
host = '10.190.208.94' # Get local machine name
port = 12346                # Reserve a port for your service.

for i in range(10):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(bytes('client connecting', 'UTF-8'))
    s.close()                     # Close the socket when done
