'''
Created on Nov 10, 2013

@author: Rex
'''

from tkinter import *
import tkinter.font as tkfont
from client.chatgui import ChatGui
from client.startup_window import StartupGui

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
        network_thread = threading.Thread(target=self.start_conn_server)
        network_thread.daemon = True
        network_thread.start()
        self.startUI()
    
    def startUI(self):
        '''
        UI thread for client; blocking
        '''
        self.root = Tk()
        
        startup_gui = StartupGui(self.root)
        
        self.root = Tk()
        self.draw_peer_frame()
        self.draw_chat_frame()
        
        self.root.mainloop()
        self.terminate()
        # self.root.destroy()
        
    def draw_peer_frame(self):
        peer_frame = Frame(self.root)
        peer_frame.grid(row=0, column=1, columnspan=1)
        title_font = tkfont.Font(family='Times', size=16, weight='bold')
        title_label = Label(peer_frame, text='All available peers:', fg='black', font=title_font)
        title_label.grid(row=0)
        
        self.peer_label_var = StringVar()
        self.peer_label = Label(peer_frame, textvariable=self.peer_label_var)
        self.peer_label.grid(row=1)
        
        label_font = tkfont.Font(family='Times', size=14)
        self.peerlist = Listbox(peer_frame, fg='#6666FF', font=label_font, relief='flat')
        self.peerlist.grid(row=2)
        
        chat_button = Button(peer_frame, text='Start Chat!')
        chat_button.grid(row=3)
        
        update_thread = threading.Timer(1, self.update_peer)
        update_thread.daemon = True
        update_thread.start()
        
    def draw_chat_frame(self):
        chat_frame = Frame(self.root, bg = '#99CCFF')
        chat_frame.grid(row=0, column=0, columnspan=1)
        gui = ChatGui(chat_frame)
        gui.create_text_display()
        
        
    def update_peer(self):
        while True:
            items = [int(x) for x in self.peerlist.curselection()]
            if len(items) > 0:
                selected_item = self.peerlist.get(items[0])
            else:
                selected_item = None
            
            self.peerlist.delete(0, END)
            for peer in self.available_peers:
                self.peerlist.insert(END, peer)
                
            # recover the selection that was deleted by the delete method
            if selected_item:
                ind = self.available_peers.index(selected_item)
                self.peerlist.activate(ind)
                self.peerlist.select_set(ind)

            # this event causes the client to fetch peer info from server
            self.update_peers_event.set()
            time.sleep(1)
        
    def start_conn_server(self):
        '''
        a separate thread for running networking tasks in background
        '''
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
