'''
Created on Nov 10, 2013

@author: Rex
'''

def create_client(ip, port):
    import client.base_client as client1
    if ip != None:
        myclient1 = client1.ChatClient(2, 'client1', ip, port)
        myclient1.start()
    else:
        print('Please specify server ip and port in the serverinfo file.')

def init_client():
    f = open('serverinfo', 'r')
    temp = f.readline().strip().split()
    ip = temp[1]
    temp = f.readline().strip().split()
    port = int(temp[1])
    print(ip, port)
    create_client(ip, port)
    
if __name__ == '__main__':
    init_client()
    #input()