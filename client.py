import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 56437 # have to matches the server port

def receive_messages(client_socket):
    """Runs on a background thread to constantly listen for incoming messages."""
    while True:
        try:
            # Buffer size 1024 bytes, decode from bytes to string
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"{message}", end="")
        except:
            print("\n[Disconnected from the server]")
            break
    
    client_socket.close()

def main():
    # 1. Connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #ipv4, tcp
    try:
        client_socket.connect((HOST, PORT))
    except Exception as e:
        print(f"Connection failed: {e}")
        return

    # 2. Choose a username
    username = input("Choose a username: ")
    # Send login command to the server
    client_socket.send(f"LOGIN {username}".encode('utf-8'))

    # 3. Handle multiple connections (Receive thread)
    recv_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    recv_thread.daemon = True # Ensures thread closes when the main program exits
    recv_thread.start()

    print("\n--- SocketChat Client Started ---")
    print("Commands:")
    print(" - Type your message and press Enter to broadcast.")
    print(" - Type '/who' to see who is connected.")
    print(" - Type '/quit' to disconnect.\n")

    # 4. Main loop for sending messages and commands
    while True:
        try:
            msg = input()
            
            #Disconnect
            if msg.lower() == '/quit':
                client_socket.send("QUIT\n".encode('utf-8'))
                client_socket.close()
                sys.exit()
            
            # who is currently online
            elif msg.lower() == '/who':
                client_socket.send("WHO/n".encode('utf-8'))
            
            # sennd public message
            elif msg:
                client_socket.send(f"SAY {msg}\n".encode('utf-8'))
                
        except KeyboardInterrupt:
            # Handle Ctrl+C cleanly
            client_socket.send("QUIT\n".encode('utf-8'))
            client_socket.close()
            sys.exit()

if __name__ == "__main__":
    main()