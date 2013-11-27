'''
Created on Nov 23, 2013

@author: Rex
'''

import tkinter
from tkinter import ttk
from client.gradient_frame import GradientFrame
from client.abstract_chatgui import AbstractChatGui

class ChatGuiImg(AbstractChatGui):
    '''
    GUI for chatting with another client
    '''


    def __init__(self, master):
        '''
        Constructor
        '''
        self.master = master;
        
    def create_text_display(self):
        display = ttk.Frame(self.master)
        display.pack(side='top')
        scrollbar = ttk.Scrollbar(display)
        self.text_display = GradientFrame(display, width=250, height=360, yscrollcommand=scrollbar.set,
                    borderwidth=0)
        # initial scroll region
        self.text_display.config(scrollregion=self.text_display.bbox(tkinter.ALL))
        scrollbar.config(command=self.text_display.yview)
        
        # text input area
        textinput = tkinter.Text(self.master, width=36, height=10, wrap='word')
        textinput.pack(side='bottom')
        textinput.insert(tkinter.END, 'Please type')
        
        # packing
        scrollbar.pack(side='right', fill='y')
        self.text_display.pack(side='left', fill='both', expand=True)
        textinput.pack(side='bottom', fill='both', expand=True)

        initmsgbox = GradientFrame(width=40, height=26, color1='#99FF99', color2='white', borderwidth=0)
        initmsgbox.create_text(2, 13, anchor='w', text='Hello')
        self.text_display.create_window(5, 20, width=40, height=26, anchor='w', window=initmsgbox)
        
        
