# server.py 
import socket                                         
import time

# create a socket object
serversocket = socket.socket(
	        socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = '192.168.1.16'                           

port = 9999                                           

# bind to the port
serversocket.bind((host, port))                                  

# queue up to 5 requests
serversocket.listen(5)                                           

while True:
    # establish a connection
    clientsocket,addr = serversocket.accept()      

    print("Got a connection from %s" % str(addr))
    currentTime = time.ctime(time.time()) + "\r\n"
    clientsocket.send(currentTime.encode('ascii'))
    try:
        msg = input() + "\r\n"
        clientsocket.send(msg.encode('ascii'))
        while True:
            msg = clientsocket.recv(10)
            print(msg)

    except KeyboardInterrupt:
        continue
    clientsocket.close()