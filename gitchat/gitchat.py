# import required modules
import socket
import threading

# creating required variable
HOST = "192.168.1.69"
PORT = 5050
ADDR = (HOST, PORT)
FORMAT = 'utf-8'

# this function listens for msgs from the server
def listen_for_msgs(client):
    while 1:
        message = client.recv(2048).decode(FORMAT)

        if message != '':
            username = message.split(" > ")[0]
            content = message.split(" > ")[1]

            print(f"[{username}] {content}")
        else:
            pass

# this function sends messages to the server
def send_msg(client):
    while 1:
        message = input("Message > ")

        if message != '':
            client.sendall(message.encode(FORMAT))
        else:
            pass

# this function communicates to the server
def communicate_to_server(client):
    username = input("Enter username > ")

    if username != '':
        client.sendall(username.encode(FORMAT))
    else:
        print(f"[SERVER] username cannot be empty")
        exit(0)
    
    threading.Thread(target=listen_for_msgs, args=(client, )).start()

    send_msg(client)

# main function
def main():
    # creating the client socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to the server
    try:
        client.connect(ADDR)
    except:
        print(f"[FATAL] unable to connect to server {ADDR}")
    
    communicate_to_server(client)

# calls the main function
if __name__ == "__main__":
    main()