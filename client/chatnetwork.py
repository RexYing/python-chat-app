'''
Created on Nov 27, 2013

@author: Rex
'''

import socket
import threading

class TcpServer(threading.Thread):
    
    # [PORT, PORT + 9] ports reserved for p2p chat
    PORT = 14285
    
    '''
    TCP server for accepting chat request
    spawn a new TcpPeer for each tcp client that requests connection
    The app is a p2p chatting app, so each client has one TcpServer running
    '''
    def __init__(self):
        '''
        Constructor
        '''
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = socket.gethostbyname(socket.gethostname())
        # bind to a random serverport between 1024 and 65536 that is available
        self.sock.bind((self.ip, 0))
        self.port = self.sock.getsockname()[1]
        self.sock.listen(5)
        
    def run(self):
        ports_used = [False * 10]
        while True:
            conn, addr = self.sock.accept()
            conn.recv(1024)
            
            # find a port that can be used
            pind = ports_used.index(False)
            available_port = pind + self.PORT + 1
            conn.send(bytes(str(available_port), 'UTF-8'))
            ports_used[pind] =True
            
            # start a TCP peer connection for that client
            tcppeer = TcpPeer(available_port)
            chat_thread = threading.Thread(target=tcppeer.start)
            chat_thread.daemon = True
            chat_thread.start()
            conn.close()
            
    def getport(self):
        return self.port
            
class TcpPeer(threading.Thread):
    '''
    A TCP host specifically for chatting with one client
    Each client can have multiple TcpPeer instances running
    '''
    
    def __init__(self, serverport):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverip = socket.gethostbyname(socket.gethostname())
        self.sock.bind((serverip, int(serverport)))
        self.sock.listen(1)
        
    def run(self):
        conn, addr = self.sock.accept()
        data = conn.recv(4096)
        print(data)
        
class TcpPeerClient(threading.Thread):
    '''
    connect to a tcp host for chatting
    '''
    
    def __init__(self, destip, destport):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.destip = destip
        self.destport = int(destport)
        
    def init_request(self):
        self.sock.connect((self.destip, self.destport))
        self.sock.send(bytes('request chat', 'UTF-8'))
        buffer = self.sock.recv(1024)
        print(buffer)
        self.sock.close()
        
    def run(self):
        self.init_request()
        