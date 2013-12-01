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
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack()
        self.tabs = {}
        
    def create_text_display(self):
        self.tabs['init'] = ChatDisplay(self.notebook, self.finishmsg)
        
        # All text display windows (for different peers) 
        # are to be added into the notebook
        self.notebook.add(self.tabs['init'].getframe(), text='Welcome')
        
    def finishmsg(self, event):
        textstr = self.tabs['init'].poll()
        self.client.sendmsg(textstr)

    def add_text(self, text, name='init'):
        self.tabs[name].add_text(text)

    def reformat(self):
        pass
    
class ChatDisplay(object):
    
    def __init__(self, master, callback):
        self.display = ttk.Frame(master)
        self.display.pack(side='top')
        scrollbar = ttk.Scrollbar(self.display)
        self.text_display = tkinter.Text(self.display, width=45, height=36, yscrollcommand=scrollbar.set,
                    wrap='word', borderwidth=0)
        scrollbar.config(command=self.text_display.yview)
        
        # text input area
        self.textinput = tkinter.Text(self.display, width=35, height=10, wrap='word')
        self.textinput.insert(tkinter.END, 'Please type')
        self.textinput.bind('<Control_L><Return>', callback)
        
        # pack
        self.textinput.pack(side='bottom', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        self.text_display.pack(side='left', fill='both', expand=True)
        
    def getframe(self):
        return self.display
        
    def add_text(self, text):
        self.text_display.insert(tkinter.END, text)
        
    def poll(self):
        textstr = self.textinput.get(1.0, tkinter.END)
        self.add_text(textstr)
        self.textinput.delete(1.0, tkinter.END)
        return textstr