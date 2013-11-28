'''
Created on Nov 23, 2013

@author: Rex
'''

import tkinter

from client.base_client import ChatClient

class StartupGui(object):
    '''
    Start up window
    For filling in name
    '''

    def __init__(self, serverip, serverport):
        '''
        start up window that allows user to enter a name
        '''
        self.root = tkinter.Tk()
        
        self.serverip = serverip
        self.serverport = serverport
        
        label = tkinter.ttk.Label(self.root, text='Your name: ')
        self.name_entry = tkinter.Entry(self.root)
        self.name_entry.focus_set()
        button = tkinter.ttk.Button(self.root, text='OK', command=self.start_client)
        
        label.grid(row=0, column=0)
        self.name_entry.grid(row=0, column=1)
        button.grid(row=1, column=0, columnspan=2)
        
        self.root.mainloop()
        
    def start_client(self):
        name = self.name_entry.get()
        if (len(name) == 0):
            # invalid name
            return
        myclient = ChatClient(2, name, self.serverip, self.serverport)
        self.root.destroy()
        myclient.start()
        