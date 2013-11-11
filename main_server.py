'''
Created on Nov 10, 2013

@author: Rex
'''

def create_server(ip, port):
    import server.udpserver as server
    server_thread = server.UdpServer(1, 'udp_chat_server', ip, port);
    server_thread.start()
    import atexit
    atexit.register(end_server, server_thread)
    
def end_server(server_thread):    
    server_thread.terminate()
    print('server is now terminated..')
    
def init_server():
    f = open('serverinfo', 'r')
    temp = f.readline().strip().split()
    ip = temp[1]
    temp = f.readline().strip().split()
    port = int(temp[1])
    create_server(ip, port)

if __name__ == '__main__':
    init_server()
    