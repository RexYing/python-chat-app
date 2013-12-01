'''
Created on Nov 27, 2013

@author: Rex
'''

import socket
import threading
import queue
import time
import tkinter

from client import coding

class ConnectionManager(threading.Thread):
    
    # [PORT, PORT + 9] ports reserved for p2p chat
    PORT = 14285
    
    # dict {peer name: tcppeer instance)
    tcppeers = {}
    
    '''
    TCP server for accepting chat request
    spawn a new TcpPeer for each tcp client that requests connection
    The app is a p2p chatting app, so each client has one ConnectionManager running
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
        ports_used = [False] * 10
        while True:
            conn, addr = self.sock.accept()
            name = coding.decode(conn.recv(1024))
            
            # find a port that can be used
            pind = ports_used.index(False)
            available_port = pind + self.PORT + 1
            conn.send(coding.encode(str(available_port)))
            ports_used[pind] = True
            
            # start a TCP peer connection for that client
            tcppeer = TcpPeer(available_port)
            self.tcppeers[name] = tcppeer
            chat_thread = threading.Thread(target=tcppeer.start)
            chat_thread.daemon = True
            chat_thread.start()
            conn.close()
            
    def getport(self):
        return self.port
    
    def fetchmsg(self):
        '''
        Fetch new messages from each tcp peer
        return a dict that maps names to new messages
        '''
        result = {}
        for name in self.tcppeers:
            msg = self.tcppeers[name].popmsg()
            if len(msg) > 0:
                result[name] = msg
        return result

class DisplayManager(threading.Thread):
    '''
    manage display of messages in chat window(s)
    '''
    
    def __init__(self, conn_manager, wins):
        '''
        wins: dict that maps names to their respective chat windows
        '''
        super().__init__()
        self.conn_manager = conn_manager
        self.wins = wins
        
    def run(self):
        while True:
            newmsg = self.conn_manager.fetchmsg()
            if newmsg:
                for name in newmsg:
                    self.wins.add_text(newmsg[name])
            time.sleep(1)
            
            
class TcpPeer(threading.Thread):
    '''
    A TCP host specifically for chatting with one client
    Each client can have multiple TcpPeer instances running
    '''
    recvmsgs = queue.Queue()
    
    def __init__(self, serverport):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverip = socket.gethostbyname(socket.gethostname())
        self.sock.bind((serverip, int(serverport)))
        self.sock.listen(1)
        
    def run(self):
        self.conn, addr = self.sock.accept()
        while True:
            # once the connection is established, recv won't block
            # even if no message is received
            msg = coding.decode(self.conn.recv(4096))
            if len(msg) > 0:
                self.recvmsgs.put(msg, block=True, timeout=5)
                print(msg)
            else:
                time.sleep(0.5)
        
    def popmsg(self):
        msg = ''
        while True:
            try:
                msg += self.recvmsgs.get_nowait()
            except queue.Empty:
                break;
        return msg
        
class TcpPeerClient(threading.Thread):
    '''
    connect to a tcp host for chatting
    '''
    
    def __init__(self, destip, destport, name):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.destip = destip
        self.destport = int(destport)
        self.name = name
        
    def init_request(self):
        self.sock.connect((self.destip, self.destport))
        self.sock.send(coding.encode(self.name))
        self.destport = int(coding.decode(self.sock.recv(1024)))
        self.sock.close()
        
    def run(self):
        self.init_request()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.destip, self.destport))
        self.sock.send(coding.encode('whatsup'))
        