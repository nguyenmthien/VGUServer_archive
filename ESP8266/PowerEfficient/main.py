import socket_server 
import time
import database

<<<<<<< HEAD
vguserver = socket_server.tcp_server(socket_server.get_ip(), 2033)
=======
vguserver = socket_server.tcp_server("192.168.100.12", 2033)
>>>>>>> b0fde00b6222840d0e9458e542ecfe77dbf0b56a
last_t = time.time()
database.createdb("thermo", "vgu.db")

def main():
    vguserver.update_sockets_list()
    try:
        vguserver.check_read_sockets()
    except socket_server.new_connection as msg:
        print(msg, end='')
        try:
            vguserver.new_socket_handler()
        except socket_server.address_does_not_exist as arg:
            id = input("Enter ID: ")
            vguserver.create_new_socket(arg.args[0], arg.args[1], id)
            print(f"Created socket with ID {id}, address {arg.args[1][0]}")
            return
        return

    message_list = vguserver.recv_all()
    
    if message_list != []:
        print(message_list)
        for dictionary in message_list:
            database.writetherm("vgu.db", dictionary['ID'], dictionary['Temp'], dictionary['Humid'])

if __name__ == '__main__':
    while True:
        main()
    