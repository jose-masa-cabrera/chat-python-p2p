import socket
import sys
import select
import json
import time

param = len(sys.argv)
HOST=socket.gethostbyname(sys.argv[1])
PORT_SERVER=int(sys.argv[2])
PORT_CLIENT=int(sys.argv[3])
SOCKET_LIST_CLIENTS = [sys.stdin]
SOCKET_LIST_CLIENTS_RECV=[]

if (param != 4):
        print ('Number of incorrect arguments peertopeer.py <IP> <PORT_SERVER> <PORT_CLIENT>')
        exit()
# Check port
if (PORT_SERVER < 1024) or (PORT_SERVER > 65535):
        print ('Port not valid!!!')
        exit()
if (PORT_CLIENT < 1024) or (PORT_CLIENT > 65535):
        print ('Port not vali!!!')
        exit()
        

server_address = ('localhost',int(PORT_SERVER))
client_address = ('localhost',int(PORT_CLIENT))




def ad_socket(SOCKET_LIST_CLIENTS_RECV):
    a = len(SOCKET_LIST_CLIENTS_RECV)
    for i in range(a):
        #socket for the chat client connections
        new_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        new_sock.connect((SOCKET_LIST_CLIENTS_RECV[i][0], SOCKET_LIST_CLIENTS_RECV[i][1]))
        SOCKET_LIST_CLIENTS.append(new_sock) 

#-----------USERNAME---------------
print('***ENTER YOUR USERNAME***')
user=input()


#-------socket------
socket_tcp =socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#---------P2P with TCP-------------
socket_tcp.bind(client_address)


socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#-------client-server With UDP----------
socket_udp.sendto((str(PORT_CLIENT)).encode("utf-8"),(server_address))
data, addr = socket_udp.recvfrom(4096)
SOCKET_LIST_CLIENTS_RECV = json.loads(data.decode())

ad_socket(SOCKET_LIST_CLIENTS_RECV)
socket_tcp.listen(10)
SOCKET_LIST_CLIENTS.append(socket_tcp)
    

print('\n ----YOU JOINED THE CHAT-----\n')

while 1:
    ready_to_read, ready_to_write, in_error = select.select(SOCKET_LIST_CLIENTS, [], [])
    
    for parameter in ready_to_read:
        if parameter is socket_tcp:
            new_conexion, addr_client = parameter.accept()
            SOCKET_LIST_CLIENTS.append(new_conexion)
            print('Connected with new user')
        else:
            if parameter is sys.stdin:
                message = input()
                if message == "exit":
                    socket_udp.sendto((str(PORT_CLIENT)).encode("utf-8"), (server_address))
                    socket_tcp.close()
                    sys.exit(0)
                else:
                    m = user + ' at ' + time.strftime("%X") + ' say: ' + message

                for p in SOCKET_LIST_CLIENTS:
                    if p!=socket_tcp and p!=parameter:
                        p.sendall(m.encode("utf-8"))
            else: 
                data = parameter.recv(1024)
                if data:
                    print(data.decode("utf-8"))
                else:
                    SOCKET_LIST_CLIENTS.remove(parameter)
                    parameter.close()
                
