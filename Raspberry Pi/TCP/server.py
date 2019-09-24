import socket
import select

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 9990
count = 0

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen()
sockets_list = [server_socket]
clients = {}

print(f'Listening for connections on {IP}:{PORT}...')

def receive_message(client_socket):
    try:
        
        mess = client_socket.recv(10)
        if not len(mess):
            return False
        return {'header': 10, 'data': mess}
    
    except:
        return False

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    for notified_socket in read_sockets:
        
        if notified_socket == server_socket:

            client_socket, client_address = server_socket.accept()
            sockets_list.append(client_socket)
            clients[client_socket] = count
            count += 1
            print('Accepted new connection from {}:{}'.format(*client_address))
            client_socket.send("abc".encode('utf-8'))
            
        else:
            
            message = receive_message(notified_socket)
            if message is False:
                
                print('Closed connection from client {} ({}:{})'.format(count,*client_address))
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            print(f'Received message: {message["data"].decode("utf-8")}')
            
    for notified_socket in exception_sockets:
        
        sockets_list.remove(notified_socket)
        del clients[notified_socket]