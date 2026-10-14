import socket, threading
from _thread import start_new_thread

def open_connection(client_socket:socket):
    pass

def assign_username(client_socket:socket, client_list:dict, username:str):
    if client_socket not in client_list:
         client_list[client_socket] = username

def broadcast_message(sender, message, client_list):
    pass


def main():
    IP_ADDRESS = "0.0.0.0"
    PORT = 56437

    server = socket.socket(socket.AF_INET, socket.SCOK_STREAM)
    server.bind((IP_ADDRESS, PORT))
    server.listen()
    print(f"The server is running on {IP_ADDRESS}:{PORT}")

    while True:
        client, addr = server.accept()
        start_new_thread(open_connection,)
