'''
Created on Dec 3, 2013

@author: yzt
'''

import socket               # Import socket module

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
host = '10.190.208.94' # Get local machine name
port = 12346                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.
while True:
    c, addr = s.accept()     # Establish connection with client.
    #print('Got connection from', addr)
    print(c.recv(1024))
    c.close()                # Close the connection
s.close()