'''
Created on Nov 23, 2013

@author: Rex
'''

import tkinter

class StartupGui(object):
    '''
    Start up window
    For filling in name
    '''


    def __init__(self, master, callback):
        '''
        master is usually the root
        callback: function to call when user is done
        '''
        
        label = tkinter.Label(master, text='Your name: ')
        name_entry = tkinter.Entry(master)
        name_entry.focus_set()
        button = tkinter.Button(master, text='OK', command=callback)
        
        label.pack(side='left')
        name_entry.pack(side='right')
        button.pack(side='bottom')