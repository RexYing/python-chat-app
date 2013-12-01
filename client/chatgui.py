'''
Created on Nov 26, 2013

@author: Rex
'''

import tkinter
from tkinter import ttk

from abc import ABCMeta, abstractmethod

class AbstractChatGui(object):
    '''
    classdocs
    '''

    __metaclass__ = ABCMeta

    def __init__(self, master):
        '''
        Constructor
        '''
        self.master = master
        
    @abstractmethod
    def create_text_display(self):
        pass
    
    @abstractmethod
    def add_text(self, text):
        pass
    
    @abstractmethod
    def reformat(self):
        pass
    
def overrides(interface_class):
    def overrider(method):
        assert(method.__name__ in dir(interface_class))
        return method
    return overrider
    
class ChatGui(AbstractChatGui):
    
    '''
    classdocs
    '''

    @overrides(AbstractChatGui)
    def __init__(self, master, client):
        '''
        Constructor
        '''
        super().__init__(master)
        self.client = client
        
    def create_text_display(self):
        
        display = ttk.Frame(self.master)
        display.pack(side='top')
        scrollbar = ttk.Scrollbar(display)
        self.text_display = tkinter.Text(display, width=45, height=36, yscrollcommand=scrollbar.set,
                    wrap='word', borderwidth=0)
        scrollbar.config(command=self.text_display.yview)
        
        # text input area
        self.textinput = tkinter.Text(display, width=35, height=10, wrap='word')
        self.textinput.insert(tkinter.END, 'Please type')
        self.textinput.bind('<Control_L><Return>', self.finishmsg)
        
        # pack
        self.textinput.pack(side='bottom', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        self.text_display.pack(side='left', fill='both', expand=True)
        
    def finishmsg(self, event):
        textstr = self.textinput.get(1.0, tkinter.END)
        self.add_text(textstr)
        self.textinput.delete(1.0, tkinter.END)
        self.client.sendmsg(textstr)

    def add_text(self, text):
        self.text_display.insert(tkinter.END, text)

    def reformat(self):
        pass
    