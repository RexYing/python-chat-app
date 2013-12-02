'''
Created on Dec 1, 2013

@author: yzt
'''

from tkinter import Text
from idlelib.WidgetRedirector import WidgetRedirector

class ReadOnlyText(Text):
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)
        self.redirector = WidgetRedirector(self)
        self.insert = self.redirector.register("insert", lambda *args, **kw: "break")
        self.delete = self.redirector.register("delete", lambda *args, **kw: "break")
        