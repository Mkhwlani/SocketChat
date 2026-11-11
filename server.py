import socket, threading
from _thread import start_new_thread

client_list = {}
clients_lock = threading.Lock()

def open_connection(client_socket:socket, client_list:dict):
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

def broadcast(sender, message):
    with clients_lock:
        targets = list(client_list.items())

    if sender not in dict(targets):
        return

    formatted_message = f"{dict(targets)[sender]}: {message}"

    print(f"[server] broadcast to {len(targets) - 1} client(s): {formatted_message}")

    for client, username in targets:
        if client != sender:
            try:
                client.sendall(formatted_message.encode('utf-8'))
            except OSError:
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
