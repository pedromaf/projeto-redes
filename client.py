from socket import *

'''
    Creates a string formatted with the nickname and the message of the sender.
    If the message text is "/leave" it will be used later as an internal command to disconnect from server.
'''
def create_message(nickname):
    message = f"{nickname}: "
    input_message = input(">> ")

    if(input_message.lower() == "/leave"):
        return ("/leave")

    return (f"{message}{input_message}")


def main():
    # Defining the server IP and Port Number to be connected.
    server_address = "127.0.0.1"
    server_port = 6666

    # Creating a socket that uses TCP and IPv4.
    client_socket = socket(family=AF_INET, type=SOCK_STREAM)

    # Nickname to identify the sender at the chat room.
    client_nickname = input("Nickname: ")

    # Starting the connection with the server.
    client_socket.connect((server_address, server_port))

    # Sending a message tagged with <JOIN> indicating the client's connection on the chat chanel.
    # The <JOIN> tag is followed by the client's nickname.
    client_socket.send(f"<JOIN>{client_nickname}".encode("utf-8"))

    # Catching a message tagged with <JOINCONFIRMATION>, confirming the client's join message.
    data = client_socket.recv(1024).decode("utf-8")
    if(data == "<JOINCONFIRMATION>"):
        print(">> You joined the chat channel! <<")

    while True:
        # Building a correctly formatted message to be send ("Nickname: msg\n").
        message = create_message(client_nickname)

        # Handles the command to end the connection with the server.
        if(message == "/leave"):
            # Sending a disconnection message to the server.
            # The message is tagged with <LEAVE> and followed by the client's nickname.
            leave_message = f"<LEAVE>{client_nickname}"
            client_socket.send(leave_message.encode("utf-8"))
            break

        # Sending the text message created at create_message() function.
        client_socket.send(message.encode("utf-8"))

        # Stores a string response from the server and prints it.
        # TODO: This will be modified in the future to receive the other clients messages redirected from the server.
        data = client_socket.recv(1024).decode("utf-8")
        if(data == "<MESSAGECONFIRMATION>"):
            continue
        else:
            print(f"{data}\n")

    # Closes the socket, ending the TCP connection with the server.
    client_socket.close()


if(__name__ == "__main__"):
    main()
