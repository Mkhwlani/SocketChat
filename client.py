import socket

HOST = "127.0.0.1"
PORT = 54532



def connect(HOST, PORT):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect(HOST, PORT)

    print("Connected to server {HOST}:{PORT}")

