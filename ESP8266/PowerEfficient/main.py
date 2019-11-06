import socket_server
import time
import database

vguserver = socket_server.tcp_server("127.0.0.1", 2033)
last_t = time.time()
database.createdb("thermo", "vgu.db")

while True:
    vguserver.update_sockets_list()
    try:
        vguserver.check_read_sockets()
    except socket_server.new_connection:
        try:
            vguserver.new_socket_handler()
        except socket_server.address_does_not_exist as arg:
            id = input("Enter ID: ")
            vguserver.create_new_socket(arg.args[0], arg.args[1], id)


    message_list = vguserver.recv_all()
    t = time.time()
    if message_list != []:
        print(message_list)
        for dictionary in message_list:
            database.writetherm("vgu.db", dictionary['ID'], dictionary['Temp'], dictionary['Humid'])
    #vguserver.send_all("abc")
    # if (t - last_t) > 30:
    #     vguserver.send_all("ab")
    #     last_t = t








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