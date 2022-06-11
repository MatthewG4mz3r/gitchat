# import required modules
import socket
import threading
import tkinter as tk # this is used to create the GUI
from tkinter import scrolledtext
from tkinter import messagebox

# creating required variable
HOST = "192.168.1.69"
PORT = 5050
ADDR = (HOST, PORT)
FORMAT = 'utf-8'

# creating the GUI variables
WIDTH  = 600
HEIGHT = 600

# colors
DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = "white"

# fonts
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)

# creating the client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def add_msg(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)

# connects the user to the server
def connect():
    # connect to the server
    try:
        client.connect(ADDR)
    except:
        message_box.showerror("connection failed", f"[FATAL] unable to connect to server {ADDR}")
        exit(0)
    add_msg("[SERVER] successfully connected to the server")

    username = username_textbox.get()

    if username != '':
        client.sendall(username.encode(FORMAT))
    else:
        message_box.showerror("invalid username", f"[SERVER] username cannot be empty")
        exit(0)
    
    threading.Thread(target=listen_for_msgs, args=(client, )).start()

def send_msg():
    message = message_textbox.get()

    if message != '':
        client.sendall(message.encode(FORMAT))
        message_textbox.delete(0, len(message))
    else:
        pass
    print("sending msg")

# creating the window
root = tk.Tk()
root.geometry(f"{WIDTH}x{HEIGHT}")
root.title("gitchat")
root.resizable(False, False)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

# creating the frames
top_frame    = tk.Frame(root, width=WIDTH, height=100, bg=DARK_GREY)
middle_frame = tk.Frame(root, width=WIDTH, height=400, bg=MEDIUM_GREY)
bottom_frame  = tk.Frame(root, width=WIDTH, height=100, bg=DARK_GREY)

top_frame.grid(row=0, column=0, sticky=tk.NSEW)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

# top frame
username_label = tk.Label(top_frame, text="Enter Username >", font=FONT, bg=DARK_GREY, fg=WHITE)
username_label.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=28)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top_frame, text="Join", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=connect)
username_button.pack(side=tk.LEFT, padx=15)

# bottom frame
message_textbox = tk.Entry(bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=48)
message_textbox.pack(side=tk.LEFT, padx=10)

message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=send_msg)
message_button.pack(side=tk.LEFT, padx=10)

# middle frame
message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=73, height=37)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)

# this function listens for msgs from the server
def listen_for_msgs(client):
    while 1:
        message = client.recv(2048).decode(FORMAT)

        if message != '':
            username = message.split(" > ")[0]
            content = message.split(" > ")[1]

            add_msg(f"[{username}] {content}")
        else:
            pass

# main function
def main():
    root.mainloop()

# calls the main function
if __name__ == "__main__":
    main()