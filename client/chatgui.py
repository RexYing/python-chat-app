'''
Created on Nov 23, 2013

@author: Rex
'''

from tkinter import *

class ChatGui(object):
    '''
    GUI for chat with another client
    '''


    def __init__(self, master):
        '''
        Constructor
        '''
        self.master  = master;
        
    def createTextWindow(self):
        self.display_text = Text(self.master)