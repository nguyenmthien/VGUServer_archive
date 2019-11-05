#!/usr/bin/env python3
# *_* coding: utf-8 *_*

"""TCP Server library"""

import socket
import select
import time
class new_connection(Exception):
    """TCP: New connection detected"""
    pass

class address_does_not_exist(Exception):
    """TCP: Address does exist in dictionary"""
    def __init__(self, *args):
        super().__init__(*args)

def receive_message(client_socket):
    """Recive message from client_socket"""
    try:
        mess = client_socket.recv(1024)
        if (not len(mess)):
            return False
        elif (len(mess) <= 2) or (mess == '\r\n'):
            return
        return mess
    
    except:
        return False

class tcp_server:
    """Create a TCP/IP Server"""
    count = 1
    #HEADER_LENGTH = 10
    def __init__(self,IP,PORT):
        self.IP = IP
        self.PORT = PORT
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.setblocking(0)
        self.server_socket.bind((self.IP, self.PORT))
        self.server_socket.listen(5)
        self.sockets_list = [self.server_socket]
        self.id_dict = {}
        self.msg = {}
        self.read_sockets = []
        self.write_sockets = []
        self.exception_sockets = []
        self.ip_dictionary = []
        

    def update_sockets_list(self):
        """Update sockets list to read_sockets, write_sockets, exception_sockets"""
        self.read_sockets, self.write_sockets, self.exception_sockets = select.select(self.sockets_list, self.sockets_list, [], 0)

    def check_read_sockets(self):
        """Handle new connection after updating socket lists"""    
        for notified_socket in self.read_sockets:
            if notified_socket == self.server_socket:
                raise new_connection('New Connection')

    def new_socket_handler(self):
        """New socket handler"""
        client_socket, client_address = self.server_socket.accept()
        client_socket.setblocking(0)
        self.sockets_list.append(client_socket)
        logic = True
        for address in self.ip_dictionary:
            if address == client_address:
                logic = False
                return

        if logic:
            raise address_does_not_exist(client_socket, client_address)

    def create_new_socket(self, client_socket, client_address, id):
        """Create new TCP socket"""
        #self.clients[client_socket] = tcp_server.count
        #tcp_server.count += 1
        self.id_dict[client_socket] = id
        self.ip_dictionary.append(client_address)
        #print(self.sockets_list)

        '''for notified_socket in self.exception_sockets:
            self.sockets_list.remove(notified_socket)
            del self.clients[notified_socket]'''
    
    def send_all(self, mess):
        for key in self.id_dict:
            if  (self.id_dict[key] != 'UPS') and (self.id_dict[key] != 'AC') and (key != self.server_socket):
                key.send(mess.encode('utf-8'))

    def therm_parsing(self, mess):
        """Split a message from a client into 2 variables"""
        mess_list = mess.split()
        if len(mess_list) == 2:
            return mess_list[0], mess_list[1]

    def recv_all(self):
        """Receive all messages from clients and parse as therm"""
        self.update_sockets_list()
        return_list = []
        for notified_socket in self.read_sockets:
            if notified_socket != self.server_socket:
                if self.id_dict[notified_socket] != 'UPS':
                    mess_dict = {'ID':self.id_dict[notified_socket]}
                    message = receive_message(notified_socket)
                    if message is False:
                        self.sockets_list.remove(notified_socket)
                        continue
                    elif message == None:
                        continue
                    message = message.strip()
                    temp, humid = self.therm_parsing(message)
                    mess_dict['Temp'] = temp.decode('utf-8')
                    mess_dict['Humid'] = humid.decode('utf-8')
                    return_list.append(mess_dict)

        return return_list