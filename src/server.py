import socket
import threading
import sys

host = socket.gethostbyname(socket.gethostname())
port = 50999
clients = []
clients_addresses = []
nicknames = []
threads = []


def create_socket():
    """
        Creates a global socket (server_socket) using TCP and IPv4 protocols.

        :return: True if the socket is created successfully otherwise, returns False.
    """
    try:
        global server_socket
        # Creating an TCP (type=SOCK_STREAM) socket using IPv4 (family=AF_INET).
        server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        print("Socket created.")
        return True
    except socket.error as msg:
        print(f"Socket creation error: {str(msg)}\n")
        return False


def bind_socket():
    """
        Binds the global server_socket to a specified address and port number and starts listening at the port.

        :return: True if binds successfully otherwise, False
    """
    try:
        print(f"Binding the port: {port} ...")

        # Providing the server IP and the server Port Number to the socket.
        server_socket.bind((host, port))

        # Opening the socket to listen to client connection.
        server_socket.listen()

        print(f"Server listening at port {port}.\n")

        return True
    except socket.error as msg:
        print(f"Socket binding error: {msg}\n")
        return False


def broadcast(message, clientSender = ""):
    for client in clients:
        if client != clientSender:
            client.send(message.encode("utf-8"))


def message_handler(message, client):
    client_index = clients.index(client)
    client_nickname = nicknames[client_index]

    if(message == "/leave"):  # Client command to leave the chat.
        # Get all client data references to remove it from the server and close the client's connection.
        client_address = clients_addresses[client_index]
        clients.remove(client)
        clients_addresses.remove(client_address)
        nicknames.remove(client_nickname)
        client.close()

        print(f"{client_nickname} disconnected!")
        broadcast(f">> {client_nickname} disconnected! <<")

        return False
    else:
        formatted_message = f"{client_nickname}:  {message}"
        broadcast(formatted_message, clients[client_index])

        return True

def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if(not message_handler(message, client)):
                break
        except:
            client_index = clients.index(client)
            clients.remove(client)
            client_nickname = nicknames[client_index]
            broadcast(f">> {client_nickname} lost connection! <<")
            nicknames.remove(client_nickname)
            client.close()
            break


def receive():
    while True:
        # Accepting clients connections.
        client, address = server_socket.accept()
        print(f"Connection established with {str(address)}")

        # Receiving client nickname.
        while True:
            try:
                client_nickname = client.recv(1024).decode("utf-8")
                if(client_nickname in nicknames):
                    client.send("FALSE".encode("utf-8"))
                else:
                    break
            except:
                print("An unexpected error has occurred!")
                sys.exit()

        # Adding the new connected client, its address and nickname to the respective lists.
        nicknames.append(client_nickname)
        clients.append(client)
        clients_addresses.append(address)

        # Broadcast to all connected clients that the new client joined the chat.
        broadcast(f">> {client_nickname} has joined the chat <<")

        # Starts a thread to handle the new client connection and saves its reference in the list.
        thread = threading.Thread(target=handle_client, args=[client])
        thread.start()
        threads.append(thread)


def main():
    if(create_socket() and bind_socket()):
        receive()


if __name__ == '__main__':
    main()