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
    def __init__(self, master):
        '''
        Constructor
        '''
        super().__init__(master)
        
    def create_text_display(self):
        display = ttk.Frame(self.master)
        display.pack(side='top')
        scrollbar = ttk.Scrollbar(display)
        self.text_display = tkinter.Text(display, width=45, height=36, yscrollcommand=scrollbar.set,
                    wrap='word', borderwidth=0)
        scrollbar.config(command=self.text_display.yview)
        
        # text input area
        textinput = tkinter.Text(self.master, width=35, height=10, wrap='word')
        textinput.insert(tkinter.END, 'Please type')
        
        # pack
        scrollbar.pack(side='right', fill='y')
        self.text_display.pack(side='left', fill='both', expand=True)
        textinput.pack(side='bottom', fill='both', expand=True)

    def add_text(self, text):
        self.text_display.insert(tkinter.END, text)

    def reformat(self):
        pass
    