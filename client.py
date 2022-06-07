from socket import *


def main():
    # Defining the server IP and Port Number to be connected.
    server_address = "127.0.0.1"
    server_port = 6666

    client_socket = socket(family=AF_INET, type=SOCK_STREAM)

    client_socket.connect((server_address, server_port))

    message = "Testando cliente-servidor."

    client_socket.send(message.encode())

    data = client_socket.recv(1024)

    print(data)

    client_socket.close()


if(__name__ == "__main__"):
    main()
