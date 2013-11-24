'''
Created on Nov 23, 2013

@author: Rex
'''

import tkinter

class GradientFrame(tkinter.Canvas):
    '''
    A gradient frame which uses a canvas to draw the background
    '''
    def __init__(self, parent=None, width=20, height=10, yscrollcommand=None,
                 color1='#CCFFFF', color2='#FFFFFF', direction='horizontal', borderwidth=0, relief="flat"):
        tkinter.Canvas.__init__(self, parent, width=width, height=height, borderwidth=borderwidth, relief=relief)
        self._color1 = color1
        self._color2 = color2
        self.direction = direction
        self.bind("<Configure>", self._draw_gradient)

    def _draw_gradient(self, event=None):
        '''
        Draw the gradient
        '''
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        if self.direction == 'vertical':
            limit = width
        else:
            limit = height
        (r1,g1,b1) = self.winfo_rgb(self._color1)
        (r2,g2,b2) = self.winfo_rgb(self._color2)
        r_ratio = float(r2-r1) / limit
        g_ratio = float(g2-g1) / limit
        b_ratio = float(b2-b1) / limit

        for i in range(limit):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = "#%4.4x%4.4x%4.4x" % (nr,ng,nb)
            if self.direction == 'vertical':
                self.create_line(i,0,i,height, tags=("gradient",), fill=color)
            else:
                self.create_line(0, i, width, i, tags=("gradient",), fill=color)
        self.lower("gradient")
        