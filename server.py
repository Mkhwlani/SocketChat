import socket, threading
from _thread import start_new_thread
client_list = {}

def open_connection(client_socket:socket):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                print(f"Received message: {message}")
                broadcast_message(client_socket, message, client_list)
        except:
            client_socket.close()
            del client_list[client_socket]
            break


def assign_username(client_socket:socket, client_list:dict, username:str):
    if client_socket not in client_list:
         client_list[client_socket] = username

def broadcast_message(sender, message, client_list):
    if sender in client_list:
        formatted_message = f"{client_list[sender]}: {message}"
        
        for client in client_list:
        
            if client != sender: 
                try:
                    client.send(formatted_message.encode('utf-8'))
                except:
                    
                    pass


def main():
    IP_ADDRESS = "0.0.0.0"
    PORT = 56437

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP_ADDRESS, PORT))
    server.listen()
    print(f"The server is running on {IP_ADDRESS}:{PORT}")

    while True:
        client, addr = server.accept()
        print(f"Connected with {addr}")
        
        client_list[client] = f"User_{addr[1]}"
        start_new_thread(open_connection, (client,))

if __name__ == "__main__":
    main()
