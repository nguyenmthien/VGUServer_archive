from socket_server import *
import time

test = server1("127.0.0.1", 9988)
check = True

while True:
    
    test.create_sockets()
    #time.sleep(1)
    client_num = int(input("Enter the client number: "))
    #client_num = 1
    test.create_sockets()
    try:
        test.sendmsg("haha", client_num)
        time.sleep(1)
        test.recvmsg(client_num)
    except:
        print("Not exist the client")