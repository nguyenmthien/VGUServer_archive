#!/usr/bin/env python3
# *_* coding: utf-8 *_*

"""An attemp to make an OOP version of example.py"""

import socket
import select
import time

def receive_message(client_socket):
    """Does this function needed?, if yes, please put a docstring in here"""
    try:
        mess = client_socket.recv(128)
        if (not len(mess)) or (len(mess) <= 2):
            return False
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
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.IP, self.PORT))
        self.server_socket.listen()
        self.sockets_list = [self.server_socket]
        self.id_dict = {}
        self.msg = {}
        self.read_sockets = []
        self.write_sockets = []
        self.exception_sockets = []
        

    def update_sockets_list(self):
        """Update sockets list to read_sockets, write_sockets, exception_sockets"""
        self.read_sockets = []
        self.write_sockets = []
        self.exception_sockets = []
        self.read_sockets, self.write_sockets, self.exception_sockets = select.select(self.sockets_list, [], self.sockets_list)

    def check_read_sockets(self):
        """Handle new connection after updating socket lists"""    
        for notified_socket in self.read_sockets:
            if notified_socket == self.server_socket:
                raise Exception('New Connection')

    def new_socket_handle(self, id):
        client_socket, client_address = self.server_socket.accept()
        self.sockets_list.append(client_socket)
        #self.clients[client_socket] = tcp_server.count
        #tcp_server.count += 1
        self.id_dict[client_socket] = id
        #print(self.sockets_list)

        '''for notified_socket in self.exception_sockets:
            self.sockets_list.remove(notified_socket)
            del self.clients[notified_socket]'''
            
    def sendmsg(self, mess, id):
        """Send a message to a specific client"""
        #self..send(mess.encode('utf-8'))
    
    def sendall(self, mess):
        for key in self.id_dict:
            if  (self.id_dict[key] != 'UPS') and (self.id_dict[key] != 'AC'):
                key.send(mess.encode('utf-8'))

    def therm_parsing(self, mess):
        """Split a message from a client into 2 variables"""
        mess_list = mess.split()
        if len(mess_list) == 2:
            return mess_list[0], mess_list[1]

    def recvall(self):
        """Receive all messages from clients"""
        return_list = []
        for notified_socket in self.read_sockets:
            if notified_socket != self.server_socket:
                if self.id_dict[notified_socket] != 'UPS':
                    mess_dict = {'ID':self.id_dict[notified_socket]}
                    message = receive_message(notified_socket)
                    if message is False:
                        self.sockets_list.remove(notified_socket)
                        continue
                    temp, humid = self.therm_parsing(message)
                    mess_dict['Temp'] = temp.decode('utf-8')
                    mess_dict['Humid'] = humid.decode('utf-8')
                    return_list.append(mess_dict)

        return return_list

    def recvmsg(self, num):
        message = receive_message(self.sockets_list[num])
        if message is False:
            print("Error")
        elif message == '':
            print("hihi")  
        else:    
            print(f'Message from client no. {num}: {message.decode("utf-8")}')
            message = ''
        #else: print("Client is closed")