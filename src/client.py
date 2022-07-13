import socket
import threading

stop_threads = False


def create_socket():
    """
        Creates a global socket (client_socket) using TCP and IPv4 protocols.

        :return: True if the socket is created successfully otherwise, returns False.
    """
    try:
        global client_socket
        # Creating an TCP (type=SOCK_STREAM) socket using IPv4 (family=AF_INET).
        client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        return True
    except socket.error as msg:
        print(f"Socket creation error: {str(msg)}\n")
        return False


def connect_server(address, port):
    # Starting the connection with the server.
    client_socket.connect((address, port))


def get_user_nickname():
    """
        Gets the nickname input from the user and returns it as a string.
        The user input can't be empty and should be between 4 and 10 characters.
    """
    while True:
        print("Enter a nickname with 4 to 10 characters.")
        nickname = input("Nickname: ")
        if(4 <= len(nickname) <= 10):
            return nickname
        else:
            print("Invalid nickname.\n")


def nickname_handler():
    global stop_threads
    while True:
        try:
            # Nickname to identify the sender at the chat room.
            client_nickname = get_user_nickname()

            # Sending nickname to be validated.
            client_socket.send(f"{client_nickname}".encode("utf-8"))

            # Validation response.
            response = client_socket.recv(1024).decode("utf-8")

            if(response == "False"):
                print("This nickname is already in use! Try another one.")
            else:
                break
        except:
            print("An unexpected error has occurred. Closing connection.")
            client_socket.close()
            stop_threads = True
            break


def create_message():
    """
        Creates a string formatted with the nickname and the message of the sender and returns it as a string.
        If the message text is an internal command, it will be returned without sender's nickname.
        The user input can't be empty.
    """
    while True:
        message = input("")
        if(len(message)):
            break

    if(message.lower() == "/leave" or message.lower().startswith("/leave ")):
        return "/leave".encode("utf-8")

    return message.encode("utf-8")


def client_receive():
    global stop_threads
    while(not stop_threads):
        try:
            message = client_socket.recv(1024).decode("utf-8")

            if(message != ""):
                print(message)
            elif(stop_threads):
                pass
            else:
                stop_threads = True
                print("An unexpected error has occurred! Closing connection.")

        except:
            stop_threads = True
            client_socket.close()
            print("An error has occurred. You got disconnected from the server!")


def client_send():
    global stop_threads
    while(not stop_threads):
        message = create_message()

        if (message == "/leave".encode("utf-8")):
            # Sending a disconnection message to the server.
            client_socket.send(message)
            stop_threads = True
        else:
            client_socket.send(message)


def main():
    # Defining the server IP and Port Number to be connected.
    server_address = "192.168.0.51"
    server_port = 50999

    create_socket()

    connect_server(server_address, server_port)

    # Sending a message that contains the client nickname.
    nickname_handler()
    print("\nYou joined the chat!")
    print("Type '/leave' to exit.\n")

    receive_thread = threading.Thread(target=client_receive)
    send_thread = threading.Thread(target=client_send)

    receive_thread.start()
    send_thread.start()

    #  receive_thread.join()
    #  send_thread.join()


if(__name__ == "__main__"):
    main()
