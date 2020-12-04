#server user P2P

import socket
import select
import sys
import time
import json
import pickle


param = len(sys.argv)
HOST = socket.gethostbyname('localhost')
PORT = int(sys.argv[1])
if (param > 2):
    print ('Usage server.py < PORT>\n',sys.argv[0])
    exit()
if ((PORT < 1024) or (PORT > 65535)):
        print ('Puerto no valido!')
        exit(1)

#Define server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#UDP
server_address = (HOST, int(PORT))
server_socket.bind(server_address)
print('-------SERVER ACTIVED-------')
SOCK_LIST=[]

while True:

    port_client, address = server_socket.recvfrom(4096)
    x=0
    port_client = (int(port_client.decode("utf-8")))
    length = len(SOCK_LIST) 
    for sock in range(length):
        if port_client == SOCK_LIST[sock][1]:
            print('CLIENT' + str(port_client) + 'NOT AVALIBLE')
            SOCK_LIST.pop(sock)
            x=1
            break
    if x == 0:
        print('NEW CLIENT CONNECTED:',port_client)
        #Send list of available sockets
        data_to_send=json.dumps(SOCK_LIST)
        server_socket.sendto(data_to_send.encode(), (address[0],address[1]))
        SOCK_LIST.append((address[0],port_client))
        print(SOCK_LIST)
    
