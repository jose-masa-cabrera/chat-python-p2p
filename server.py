#server user P2P

import socket
import select
import sys
import time
import json
import pickle

# Comprobamos el numero de argumentos
param = len(sys.argv)
HOST = socket.gethostbyname('localhost')
PORT = int(sys.argv[1])
if (param > 2):
    print ('Usage server.py < PORT>\n',sys.argv[0])
    exit()
if ((PORT < 1024) or (PORT > 65535)):
        print ('Puerto no valido!')
        exit(1)

#Definimos el socket servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#UDP
server_address = (HOST, int(PORT))
server_socket.bind(server_address)
print('-------SERVER ACTIVED-------')
SOCK_LIST=[]#creamos una lista donde guardaremos la lista de sockets clientes disponibles

while True:

    port_client, address = server_socket.recvfrom(4096)# El valor de retorno es un par (bytes(puerto del cliente), dirección) donde bytes es un objeto de bytes que representa los datos recibidos(puerto del cliente) y dirección es la dirección del socket que envía los datos.
    #recorreremos la lista para ver si es un nuevo socket
    x=0
    port_client = (int(port_client.decode("utf-8")))#nos llegan bytes decodificamos y obtenemos un valor entero de tipo int
    length = len(SOCK_LIST) # obtenemos la longitud de la lista
    for sock in range(length):
        if port_client == SOCK_LIST[sock][1]:
            print('CLIENT' + str(port_client) + 'NOT AVALIBLE')
            SOCK_LIST.pop(sock)#eliminamos el puerto del cliente que se ha marchado
            x=1
            break
    if x is 0:
        print('NEW CLIENT CONNECTED:',port_client)
        #enviamos la lista de los sockets disponibles
        data_to_send=json.dumps(SOCK_LIST)#enviamos la lista
        server_socket.sendto(data_to_send.encode(), (address[0],address[1]))
        SOCK_LIST.append((address[0],port_client))
        print(SOCK_LIST)
    
