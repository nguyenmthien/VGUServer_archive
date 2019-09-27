import socket_server
import time

vguserver = socket_server.tcp_server("192.168.1.4", 2033)
last_t = time.time()

while True:
    vguserver.update_sockets_list()
    try:
        vguserver.check_read_sockets()
    except:
        id = input("Enter ID: ")
        vguserver.new_socket_handle(id)    
    message_list = vguserver.recvall()
    if message_list != []:
        print(message_list)
    vguserver.sendall("abc")
    '''t = time.time()
    if (t - last_t) > 3:
        vguserver.sendall("abc")
        last_t = t'''








    '''test.create_sockets()
    client_num = int(input("Enter the client number: "))
    test.create_sockets()
    try:
        test.sendmsg("haha", client_num)
        time.sleep(1)
        test.recvmsg(client_num)

        s= time.time()

    except:
        print("The client does not exist!")
        socket_server.tcp_server()'''