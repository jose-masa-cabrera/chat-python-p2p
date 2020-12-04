import socket
import sys
import select
import json
import time

param = len(sys.argv)
HOST=socket.gethostbyname(sys.argv[1])
PORT_SERVER=int(sys.argv[2])
PORT_CLIENT=int(sys.argv[3])
SOCKET_LIST_CLIENTS = [sys.stdin]#lista para las conexiones entre peers
SOCKET_LIST_CLIENTS_RECV=[]#lista recibida del servidor de usuarios

if (param != 4):
        print ('Numero de argumentos incorrectos  peertopeer.py <IP> <PORT_SERVER> <PORT_CLIENT>')
        exit()
# Comprobamos el puerto
if (PORT_SERVER < 1024) or (PORT_SERVER > 65535):
        print ('Puerto no valido!!!')
        exit()
if (PORT_CLIENT < 1024) or (PORT_CLIENT > 65535):
        print ('Puerto no valido!!!')
        exit()
        

server_address = ('localhost',int(PORT_SERVER))
client_address = ('localhost',int(PORT_CLIENT))




def ad_socket(SOCKET_LIST_CLIENTS_RECV):
    a = len(SOCKET_LIST_CLIENTS_RECV)
    for i in range(a):
        #socket para conexiones con clientes del chat
        new_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        new_sock.connect((SOCKET_LIST_CLIENTS_RECV[i][0], SOCKET_LIST_CLIENTS_RECV[i][1]))
        SOCKET_LIST_CLIENTS.append(new_sock) #se van añadiendo a los clientes

#-----------Nombre de usuario---------------
print('***INTRODUCE TU NOMBRE DE USUARIO***')
user=input()


#-------socket------
socket_tcp =socket.socket(socket.AF_INET, socket.SOCK_STREAM)#para comunicación P2P es decir para actuar como servidor de otros peers
#---------P2P with TCP-------------
socket_tcp.bind(client_address)#escuchamos solicitudes entrantes en IP y puerto cliente


socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#para el server
#-------client-server With UDP----------
#enviamos al servidor nuestro numero de puerto
socket_udp.sendto((str(PORT_CLIENT)).encode("utf-8"),(server_address))
data, addr = socket_udp.recvfrom(4096)
SOCKET_LIST_CLIENTS_RECV = json.loads(data.decode())#recibimos la lista del servidor

ad_socket(SOCKET_LIST_CLIENTS_RECV)
socket_tcp.listen(10)#pongo a la escucha el socket para los peers
SOCKET_LIST_CLIENTS.append(socket_tcp)#agregamos la nueva conexion a la lista de conexiones
    

print('\n ----Te has unido al grupo-----\n')

while 1:
    #print('función antes del select')
    ready_to_read, ready_to_write, in_error = select.select(SOCKET_LIST_CLIENTS, [], [])
    
    for parameter in ready_to_read:#socket que estan listos para leer
        if parameter is socket_tcp:#un peer quiere conectarse a nosotros
            new_conexion, addr_client = parameter.accept()#acepto la conexión del peer
            SOCKET_LIST_CLIENTS.append(new_conexion)#agrego la nueva conexión
            print('Connected with new user')
        else:
            if parameter is sys.stdin:#se activa el socket del teclado
                message = input()
                if message == "exit":
                    socket_udp.sendto((str(PORT_CLIENT)).encode("utf-8"), (server_address))
                    socket_tcp.close()
                    sys.exit(0)
                else:
                    m = user + ' at ' + time.strftime("%X") + ' say: ' + message

                for p in SOCKET_LIST_CLIENTS:#recorro la lista de los socket
                    if p!=socket_tcp and p!=parameter:
                        p.sendall(m.encode("utf-8"))
            else: #si recibimos datos
                data = parameter.recv(1024)
                if data:#si recibimos algo
                    print(data.decode("utf-8"))
                else:
                    SOCKET_LIST_CLIENTS.remove(parameter)
                    parameter.close()
                
