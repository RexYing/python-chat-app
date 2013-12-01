'''
Created on Nov 30, 2013

@author: yzt
'''

class Coding(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
    def encode(self, string):
        return bytes(string, 'UTF-8')
    
    def decode(self, bytearr):
        return bytearr.decode('UTF-8')
    
coding = Coding()

def encode(string):
    return coding.encode(string)

def decode(bytearr):
    return coding.decode(bytearr)
