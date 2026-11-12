import socket, threading
from _thread import start_new_thread
import re

NAME_RULE = re.compile(r"^[a-zA-Z0-9_]{1,12}$")
client_list = {}
clients_lock = threading.Lock()



def handle(client_socket: socket.socket, addr):
    tag = threading.current_thread().name
    print(f"[{tag}] connection from {addr}")

    try:
        with client_socket, client_socket.makefile("r", encoding="utf-8", errors="replace", newline="\n") as lines:
            for line in lines:
                text = line.strip()

                if not text:
                    continue

                print(f"[{tag}] received from {addr}: {text}")
                command, _, rest = text.partition(" ")
                command = command.upper()

                if command == "LOGIN":
                    if client_socket in client_list:
                        client_socket.sendall("ERROR you are already logged in\n".encode("utf-8"))

                    elif not NAME_RULE.fullmatch(rest):
                        client_socket.sendall("ERROR name must be 1 to 12 letters, digits or _\n".encode("utf-8"))

                    else:
                        with clients_lock:
                            taken = rest in client_list.values()

                            if not taken:
                                client_list[client_socket] = rest

                        if taken:
                            client_socket.sendall("ERROR name already taken\n".encode("utf-8"))
                        else:
                            client_socket.sendall(f"OK logged in as {rest}\n".encode("utf-8"))
                            broadcast(client_socket, f"INFO {rest} joined")

                elif command == "QUIT":
                    client_socket.sendall("BYE\n".encode("utf-8"))
                    break

                elif client_socket not in client_list:
                    client_socket.sendall("ERROR login first: LOGIN <name>\n".encode("utf-8"))

                elif command == "SAY":
                    if rest:
                        broadcast(client_socket, rest)
                    else:
                        client_socket.sendall("ERROR nothing to say\n".encode("utf-8"))

                elif command == "WHO":
                    with clients_lock:
                        names = ",".join(sorted(client_list.values()))
                    client_socket.sendall(f"USERS {names}\n".encode("utf-8"))

                else:
                    client_socket.sendall("ERROR unknown command (LOGIN, SAY, WHO, QUIT)\n".encode("utf-8"))

    except (ConnectionResetError, BrokenPipeError):
        print(f"[{tag}] {addr} dropped the connection")



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
