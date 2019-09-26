#!/usr/bin/env python3
# *_* coding: utf-8 *_*

"""An attemp to make an OOP version of example.py"""

import socket
import select
import time

def receive_message(client_socket):
    """Does this function needed?, if yes, please put a docstring in here"""
    try:
        mess = client_socket.recv(10)
        if not len(mess):
            return False
        return mess
    
    except:
        return False

class tcp_server:
    """This is a docstring"""
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
        self.clients = {}
        self.msg = {}
        
    def create_sockets(self):
        read_sockets, _, exception_sockets = select.select(self.sockets_list, [], self.sockets_list)
        
        for notified_socket in read_sockets:
            if notified_socket == self.server_socket:
        
                client_socket, client_address = self.server_socket.accept()
                self.sockets_list.append(client_socket)
                self.clients[client_socket] = tcp_server.count
                tcp_server.count += 1
                #print(self.sockets_list)
                
        for notified_socket in exception_sockets:
            self.sockets_list.remove(notified_socket)
            del self.clients[notified_socket]
            
    def sendmsg(self, mess, num):
        
        self.sockets_list[num].send(mess.encode('utf-8'))
        
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