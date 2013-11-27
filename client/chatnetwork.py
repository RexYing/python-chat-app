'''
Created on Nov 27, 2013

@author: yzt
'''

import socket

class TcpServer(object):
    '''
    classdocs
    '''
    
    PORT = 14285

    def __init__(self):
        '''
        Constructor
        '''
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip = socket.gethostbyname(socket.gethostname())
        self.sock.bind((ip, self.PORT))
        self.sock.listen(5)
        
    def start(self):
        ports_used = [False * 10]
        while True:
            conn, addr = self.sock.accept()
            conn.recv(1024)
            pind = ports_used.index(False)
            conn.send(str(pind + self.PORT + 1))
            conn.close()
            
class TcpPeer(object):
    
    def __init__(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip = socket.gethostbyname(socket.gethostname())
        self.sock.bind((ip, port))
        self.sock.listen(1)
        
    def start(self):
        conn, addr = self.sock.accept()
        data = conn.recv(4096)
        print(data)