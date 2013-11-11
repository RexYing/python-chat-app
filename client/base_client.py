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

    def initsocket(self, ip, port):
        self.server_addr = (ip, port)
        print('Client ', self.name, ': try to reach ', self.server_addr)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def run(self):
        ui_thread = threading.Thread(target=self.start_network)
        ui_thread.start()
        self.startUI()
        
    '''
    UI thread for client
    '''
    def startUI(self):
        self.root = Tk()
        self.root.mainloop()
        
    '''
    a separate thread for running networking tasks in background
    '''
    def start_network(self):
        # send request
        time.sleep(0.5)
        request = self.name + ' ls'
        self.sock.sendto(bytes(request, 'UTF-8'), self.server_addr)
        # receive list of other clients
        peerinfo, addr = self.sock.recvfrom(self.MAX_LENGTH)
        peerinfo = peerinfo.decode('UTF-8').split(';')
        for peer_str in peerinfo:
            print('Client ', self.name, ': received ', peer_str)
        #
        #self.terminate()

    def terminate(self):
        print('client closing')
        self.sock.close()        
