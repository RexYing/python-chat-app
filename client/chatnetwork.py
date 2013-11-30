'''
Created on Nov 27, 2013

@author: yzt
'''

import socket
import threading

class TcpServer(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = socket.gethostbyname(socket.gethostname())
        # bind to a random serverport between 1024 and 65536 that is available
        self.sock.bind((self.ip, 0))
        self.port = self.sock.getsockname()[1]
        self.sock.listen(5)
        
    def start(self):
        ports_used = [False * 10]
        while True:
            conn, addr = self.sock.accept()
            conn.recv(1024)
            
            # find a port that can be used
            pind = ports_used.index(False)
            available_port = pind + self.PORT + 1
            conn.send(str(available_port))
            ports_used[pind] =True
            
            # start a TCP peer connection for that client
            tcppeer = TcpPeer(available_port)
            chat_thread = threading.Thread(target=tcppeer.start)
            chat_thread.daemon = True
            chat_thread.start()
            conn.close()
            
    def getport(self):
        return self.port
            
class TcpPeer(object):
    
    def __init__(self, serverport):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverip = socket.gethostbyname(socket.gethostname())
        self.sock.bind((serverip, serverport))
        self.sock.listen(1)
        
    def start(self):
        conn, addr = self.sock.accept()
        data = conn.recv(4096)
        print(data)