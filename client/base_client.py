'''
Created on Nov 10, 2013

@author: Rex
'''

from tkinter import *
import socket
import threading
import time

class ChatClient(threading.Thread):
    '''
    base class of client
    '''

    MAX_LENGTH = 1024

    def __init__(self, threadID, name, ip, port):
        '''
        Constructor
        '''
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.initsocket(ip, port)
        self.available_peers = []
        self.update_peers_event = threading.Event()

    def initsocket(self, ip, port):
        self.server_addr = (ip, port)
        print('Client ', self.name, ': try to reach ', self.server_addr)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def run(self):
        network_thread = threading.Thread(target=self.start_network)
        network_thread.daemon = True
        network_thread.start()
        self.startUI()
        
    '''
    UI thread for client; blocking
    '''
    def startUI(self):
        self.root = Tk()
        peer_frame = Frame(self.root)
        peer_frame.pack(side=RIGHT)
        
        self.peer_label_var = StringVar(value='Looking for peers...')
        self.peer_label = Label(self.root, textvariable=self.peer_label_var)
        self.peer_label.pack()
        update_thread = threading.Timer(1, self.update_peer)
        update_thread.start()
        
        self.root.mainloop()
        self.terminate()
        # self.root.destroy()
        
    def update_peer(self):
        temp = ''
        for peer in self.available_peers:
            temp += peer + '\n'
        self.peer_label_var.set(temp);
        # re-register timer
        update_thread = threading.Timer(1, self.update_peer)
        update_thread.start()
        self.update_peers_event.set()
        
    '''
    a separate thread for running networking tasks in background
    '''
    def start_network(self):
        while True:
            self.update_peers_event.wait()
            # send request
            request = self.name + ' ls'
            self.sock.sendto(bytes(request, 'UTF-8'), self.server_addr)
            # receive list of other clients
            peerinfo = self.sock.recvfrom(self.MAX_LENGTH)[0]
            peerinfo = peerinfo.decode('UTF-8').split(';')
            self.available_peers = []
            for peer_str in peerinfo:
                peer_str.strip()
                self.available_peers.append(peer_str)
                print('Client ', self.name, ': received ', 'No peers' if not peer_str else peer_str);
                # notify GUI to update available peers
                self.update_peers_event.clear()

    def terminate(self):
        # Tell server that this client terminates
        request = self.name + ' exit'
        self.sock.sendto(bytes(request, 'UTF-8'), self.server_addr)
        self.sock.close()        
