from socket import *


def main():
    # Defining the port number and the server IP address.
    server_port = 6666
    server_address = "127.0.0.1"

    # Creating an TCP (type=SOCK_STREAM) socket using IPv4 (family=AF_INET).
    server_socket = socket(family=AF_INET, type=SOCK_STREAM)

    # Providing the server IP and the server Port Number to the socket.
    server_socket.bind((server_address, server_port))

    # Opening the socket to listen to client connection.
    server_socket.listen()

    while True:
        (client_socket, client_address) = server_socket.accept()

        while True:
            data = client_socket.recv(1024)

            if(data != b''):
                print(data)
                message = "Testando servidor-cliente."
                client_socket.send(message.encode())
                break


if __name__ == '__main__':
    main()
