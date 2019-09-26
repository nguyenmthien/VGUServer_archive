import socket_server
import time

test = socket_server.tcp_server("192.168.1.7", 2033)

while True:
    
    test.create_sockets()
    client_num = int(input("Enter the client number: "))
    test.create_sockets()
    try:
        test.sendmsg("haha", client_num)
        time.sleep(1)
        test.recvmsg(client_num)
    except:
        print("The client does not exist!")