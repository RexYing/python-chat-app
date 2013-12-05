'''
Created on Nov 26, 2013

@author: Rex
'''

import tkinter
from tkinter import ttk

from abc import ABCMeta, abstractmethod

from client.text_ext import ReadOnlyText

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
        # maps tab_id to ChatDisplay instance
        self.tab_id_to_display = {}
        # map user_id to tab_id
        self.id_to_tab_id = {}
        self.leftover = {}
        
    def create_text_display(self):
        tab = ChatDisplay(self.notebook, self.finishmsg)
        
        # All text display windows (for different peers) 
        # are to be added into the notebook
        self.notebook.add(tab.getframe(), text='Welcome')
        self.tab_id_to_display[self.notebook.select()] = tab
        self.id_to_tab_id[0] = self.notebook.tabs()[self.notebook.index('end') - 1]
        
        # bind virtual event
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_selected)
        
    def addtab(self, user_id, show=False):
        '''
        user_id: the id of the other peer that the user is chatting with
        '''
        if user_id in self.id_to_tab_id:
            # already existed but might be hidden
            display = self.tab_id_to_display[self.id_to_tab_id[user_id]]
            self.notebook.add(display.getframe())
            return
            
        tab = ChatDisplay(self.notebook, self.finishmsg, user_id)
        self.notebook.add(tab.getframe(), text='User '+user_id)
        tab_id = self.notebook.tabs()[self.notebook.index('end') - 1]
        self.tab_id_to_display[tab_id] = tab
        self.id_to_tab_id[user_id] = tab_id
        if show:
            self.notebook.select(tab_id)

    def finishmsg(self, event):
        textstr = self.tab_id_to_display[self.notebook.select()].poll()
        self.client.sendmsg(textstr)

    def add_text(self, text, user_id=0):
        '''
        add text for user_id
        '''
        if not user_id in self.id_to_tab_id:
            self.leftover[user_id] = text
            welcome_display = self.tab_id_to_display[self.id_to_tab_id[0]]
            welcome_display.add_text(user_id + ' wants to chat with you:)\n\n')
            return
        tab_id = self.id_to_tab_id[user_id]
        self.tab_id_to_display[tab_id].add_text(text)
        
    def closewin(self):
        self.notebook.hide(self.notebook.select())

    def reformat(self):
        pass
    
    def on_right_click(self, event):
        # right click on tab. currently not used
        if event.widget.identify(event.x, event.y) == 'label':
            index = event.widget.index('@%d,%d' % (event.x, event.y))
            print(event.widget.tab(index, 'text'))
            
    def on_tab_selected(self, event):
        user_id = self.tab_id_to_display[self.notebook.select()].getdestuser()
        self.client.change_active_dest(user_id)
        print('switch to user', user_id)
    
class ChatDisplay(object):
    
    def __init__(self, master, callback, dest_user=None):
        self.dest_user = dest_user
        
        self.display = ttk.Frame(master)
        self.display.pack(side='top')
        scrollbar = ttk.Scrollbar(self.display)
        self.text_display = ReadOnlyText(self.display, width=45, height=36, yscrollcommand=scrollbar.set,
                    wrap='word', borderwidth=0)
        scrollbar.config(command=self.text_display.yview)
        
        # text input area
        self.textinput = tkinter.Text(self.display, width=35, height=10, wrap='word')
        self.textinput.bind('<Control_L><Return>', callback)
        if not dest_user:
            # if no dest_user (Welcome window), disable textinput
            self.textinput.insert(tkinter.END, 'Select a peer first')
            self.textinput.config(state='disabled')
        else:
            self.textinput.insert(tkinter.END, 'Please type')
        
        # pack
        self.textinput.pack(side='bottom', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        self.text_display.pack(side='left', fill='both', expand=True)
        
    def getdestuser(self):
        return self.dest_user
        
    def getframe(self):
        return self.display
    
    def is_sysmsg(self, text):
        # check if it is system message
        try:
            if text.index('SYS') == 0:
                return True
        except ValueError:
            pass
        return False
        
    def add_text(self, text, mine=False):
        text = text.strip(' \n')
        if self.dest_user:
            if self.is_sysmsg(text):
                author = ''
            elif mine:
                author = 'I said:\n'
            else:
                author = self.dest_user + ' said:\n'
            text = author + text + '\n\n\n'
        else:
            # welcome messages do not have user_id
            text = text + '\n\n'
        self.text_display.insert(tkinter.END, text)
        
    def poll(self):
        '''
        Return the text in its textinput
        Also add the text to its own display window
        '''
        textstr = self.textinput.get(1.0, tkinter.END)
        self.add_text(textstr, mine=True)
        self.textinput.delete(1.0, tkinter.END)
        return textstr