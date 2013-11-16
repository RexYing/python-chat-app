'''
Created on Nov 10, 2013

@author: Rex
'''

import threading
import socket

class UdpServer(threading.Thread):
    '''
    Server that provides a list of available clients upon request
    '''

    DEFAULT_BACKLOG = 5
    MAX_LENGTH = 1024
    
    client_list = {}

    def __init__(self, threadID, name, ip, port):
        '''
        Constructor
        '''
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.initsocket(ip, port)
        
    def initsocket(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = ip
        self.port = port
        print('Server: Running on ', self.host, self.port)
        
        self.sock.bind((self.host, self.port))
        
    def ls(self, addr):
        response = ''
        print(self.client_list)
        # send back all available client except the requesting client
        for iaddr in self.client_list:
            if iaddr != addr:
                response += str(self.client_list[iaddr]['name'] + ';')
        response = response[: -1]
        self.sock.sendto(bytes(response, 'UTF-8'), addr)
        
    def client_exit(self, addr):
        # exclude from client_list
        self.client_list.pop(addr)
        
    def run(self):
        print('Server: ready...')

        while True:
            request, addr = self.sock.recvfrom(self.MAX_LENGTH)
            req_str = request.decode('UTF-8')
            print('Server: received: ', req_str, addr)
            info = req_str.split()
            self.client_list[addr] = {'name': info[0]}
            handle = {   
                'ls': self.ls,
                'exit': self.client_exit
                }.get(info[1])
            handle(addr)
        
    def terminate(self):
        self.sock.close()
