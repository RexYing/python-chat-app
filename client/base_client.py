'''
Created on Nov 10, 2013

@author: Rex
'''

import tkinter
import tkinter.font as tkfont
from tkinter import ttk
from client.chatgui import ChatGui
import client.chatnetwork as chatnetwork

import socket
import threading
import time

class ChatClient(threading.Thread):
    '''
    base class of client
    '''

    MAX_LENGTH = 1024

    def __init__(self, threadID, name, serverip, serverport):
        '''
        Constructor
        '''
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.initsocket(serverip, serverport)
        self.available_peers = []
        self.update_peers_event = threading.Event()

    def initsocket(self, ip, port):
        self.server_addr = (ip, port)
        print('Client ', self.name, ': try to reach ', self.server_addr)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def run(self):
        self.conn_manager = chatnetwork.ConnectionManager(self)
        self.conn_manager.daemon = True
        self.client_tcpport = self.conn_manager.getport()
        self.conn_manager.start()
        
        query_server_thread = threading.Thread(target=self.start_conn_server)
        query_server_thread.daemon = True
        query_server_thread.start()
        
        self.startUI()
    
    def startUI(self):
        '''
        UI thread for client; blocking
        '''

        self.root = tkinter.Tk()
        self.draw_peer_frame()
        self.draw_chat_frame()
        
        self.root.mainloop()
        self.terminate()
        # self.root.destroy()
        
    def draw_peer_frame(self):
        peer_frame = ttk.Frame(self.root)
        peer_frame.grid(row=0, column=1, columnspan=1)
        title_font = tkfont.Font(family='Times', size=16, weight='bold')
        title_label = ttk.Label(peer_frame, text='All available peers:', font=title_font)
        title_label.grid(row=0)
        
        self.peer_label_var = tkinter.StringVar()
        self.peer_label = ttk.Label(peer_frame, textvariable=self.peer_label_var)
        self.peer_label.grid(row=1)
        
        label_font = tkfont.Font(family='Times', size=14)
        self.peerlist = tkinter.Listbox(peer_frame, fg='#6666FF', font=label_font, relief='flat')
        self.peerlist.grid(row=2)
        
        chat_button = ttk.Button(peer_frame, text='Start Chat!', command=self.request_chat)
        chat_button.grid(row=3)
        
        update_thread = threading.Timer(1, self.update_peer)
        update_thread.daemon = True
        update_thread.start()
        
    def request_chat(self):
        items = [int(x) for x in self.peerlist.curselection()]
        peerid = self.peerlist.get(items[0])
        self.conn_manager.setactivedest(peerid)
        if not peerid in self.conn_manager.tcppeers:
            # connect if not already connected
            ip, port = self.available_peers[peerid]
            self.conn_manager.add_peer_client(self.name, ip, port)
        # add a tab for that guy
        self.chatgui.addtab(peerid, show=True)
        
    def draw_chat_frame(self):
        #chat_frame = ttk.Frame(self.root, bg = '#99CCFF')
        chat_frame = ttk.Frame(self.root)
        chat_frame.grid(row=0, column=0, columnspan=1)
        self.chatgui = ChatGui(chat_frame, self)    
        self.chatgui.create_text_display()
        self.chatgui.add_text('Hello ' + self.name + '\n')
        
        # set display manager which periodically update all messages received
        # from self.conn_manager to ChatGui instance
        dispmanager = chatnetwork.DisplayManager(self.conn_manager, self.chatgui)
        dispmanager.daemon = True
        dispmanager.start()
        
    def sendmsg(self, text):
        '''
        Relay text obtained from GUI to network
        '''
        self.conn_manager.sendmsg(text)
        
    def update_peer(self):
        while True:
            items = [int(x) for x in self.peerlist.curselection()]
            if len(items) > 0:
                selected_item = self.peerlist.get(items[0])
            else:
                selected_item = None
            
            self.peerlist.delete(0, tkinter.END)
            for peer in self.available_peers:
                # include name in the list
                self.peerlist.insert(tkinter.END, peer)
                # recover the selection that was deleted by the delete method
                if (peer == selected_item):
                    self.peerlist.activate(tkinter.END)
                    self.peerlist.select_set(tkinter.END)
                

            # this event causes the client to fetch peer info from server
            self.update_peers_event.set()
            time.sleep(2)
        
    def start_conn_server(self):
        '''
        a separate thread for running networking tasks in background
        '''
        request = self.name + ' login ' + str(self.client_tcpport)
        self.sock.sendto(bytes(request, 'UTF-8'), self.server_addr)
        while True:
            self.update_peers_event.wait()
            # send request
            request = self.name + ' ls'
            self.sock.sendto(bytes(request, 'UTF-8'), self.server_addr)
            # receive list of other clients
            peerinfo = self.sock.recvfrom(self.MAX_LENGTH)[0]
            peerinfo = peerinfo.decode('UTF-8').split(';')
            self.available_peers = {}
            self.update_peers_event.clear()
            for peer_str in peerinfo:
                # peerinfo contains fields: ip, port and name
                info = peer_str.strip().split()
                if (len(info) == 0):
                    continue
                self.available_peers[info[2]] = ((info[0], info[1]))
                # notify GUI to update available peers
                

    def terminate(self):
        # Tell server that this client terminates
        request = self.name + ' exit'
        self.sock.sendto(bytes(request, 'UTF-8'), self.server_addr)
        self.sock.close()        
