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
    
    # dict {peer name: tcppeer instance connecting to that peer)
    tcppeers = {}
    
    '''
    TCP server for accepting chat request
    spawn a new Peer for each tcp client that requests connection
    The app is a p2p chatting app, so each client has one ConnectionManager running
    '''
    def __init__(self, client=None):
        '''
        Constructor
        '''
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.ip = socket.gethostbyname(socket.gethostname())
        # bind to a random serverport between 1024 and 65536 that is available
        self.sock.bind(('0.0.0.0', 0))
        self.port = self.sock.getsockname()[1]
        self.sock.listen(5)
        self.client = client
        print('my own: ', self.sock.getsockname()[0], self.port)
        
    def run(self):
        print('p2p chat available')
        while True:
            conn, addr = self.sock.accept()
            name = coding.decode(conn.recv(1024))
            
            # start a TCP peer connection for that client
            tcppeer = Peer()
            conn.send(coding.encode(str(tcppeer.getport())))
            self.tcppeers[name] = tcppeer
            chat_thread = threading.Thread(target=tcppeer.start)
            chat_thread.daemon = True
            chat_thread.start()
            conn.close()
            
            #switch the active dest to the recently connected one
            self.active_dest = name
            
    def add_peer_client(self, myname, destip, destport):
        '''
        add a PeerClient intance connecting to self.active_dest
        '''
        tcpclient = PeerClient(destip, destport, myname)
        self.tcppeers[self.active_dest] = tcpclient
        tcpclient.daemon = True
        tcpclient.start()
            
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
    
    def sendmsg(self, text):
        '''
        Send new messages that user typed in to a peer specified by its name
        '''
        self.tcppeers[self.active_dest].send(text)
    
    def quitchat(self):
        self.tcppeers[self.active_dest].quit()
        self.tcppeers.pop(self.active_dest)
        
    def quitall(self):
        print('p2p chat closed')
        for peer in self.tcppeers:
            self.tcppeers[peer].quit()
        self.sock.close()
        
    def setactivedest(self, destname):
        self.active_dest = destname
        
    def getactivedest(self):
        return self.active_dest
        

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
            print(newmsg)
            if newmsg:
                for name in newmsg:
                    self.wins.add_text(newmsg[name], name)
            time.sleep(1)
            
class AbstractPeer(threading.Thread):
    
    recvmsgs = queue.Queue()
    
    def __init__(self):
        super().__init__()
        self.num_msg = 0
        self.total_rtt = 0
    
    def popmsg(self):
        msg = ''
        while True:
            try:
                msg += self.recvmsgs.get_nowait()
            except queue.Empty:
                break;
        return msg
    
    def is_ack(self, text):
        try:
            if text.index('ACK') == 0:
                return True
        except ValueError:
            pass
        return False
    
    def get_rtt(self):
        self.total_rtt += time.time() - self.starttime
        self.num_msg += 1
        return self.total_rtt / self.num_msg
    
    def parsemsg(self, msg):
        if len(msg) > 0:
            # check if this is ACK first
            if self.is_ack(msg):
                print('Acknowledgement received: ', msg)
                print('TCP rtt:', self.get_rtt())
                return
            self.recvmsgs.put(msg, block=True, timeout=5)
            # send ACK
            self.send('ACK ' + msg)
        else:
            time.sleep(0.5)
    
    def quit(self):
        pass
            
class Peer(AbstractPeer):
    '''
    A TCP endpoint specifically for chatting with one client
    Each client can have multiple Peer instances running
    '''
    
    def __init__(self):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #serverip = socket.gethostbyname(socket.gethostname())
        self.sock.bind(('0.0.0.0', 0))
        self.sock.listen(1)
        
    def run(self):
        self.conn, addr = self.sock.accept()
        print(addr)
        while True:
            # once the connection is established, recv won't block
            # even if no message is received
            try:
                msg = coding.decode(self.conn.recv(4096))
            except:
                self.sock.close()
                return
            self.parsemsg(msg)
                
    def send(self, text):
        try:
            if not self.is_ack(text):
                self.starttime = time.time()
            self.conn.send(coding.encode(text))
            print('send from ', self.sock.getsockname()[1])
        except:
            return
        
    def getport(self):
        # get own socket
        return self.sock.getsockname()[1]
    
    def quit(self):
        self.sock.close()
        
class PeerClient(AbstractPeer):
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
        while True:
            try:
                msg = coding.decode(self.sock.recv(4096))
            except:
                self.sock.close()
                return
            self.parsemsg(msg)
        
    def send(self, text):
        try:
            if not self.is_ack(text):
                self.starttime = time.time()
            self.sock.send(coding.encode(text))
        except:
            # the other peer's socket closed
            return
        
    def getport(self):
        # get destination port
        return self.destport
        
    def quit(self):
        self.sock.close()