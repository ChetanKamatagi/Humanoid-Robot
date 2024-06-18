import socket

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Specify the server's address and port
server_address = ('10.4.2.187', 12345)  # Replace with the actual server IP

# Connect to the server
client_socket.connect(server_address)

# Receive the welcome message from the server
welcome_message = client_socket.recv(1024)
print(f"Server says: {welcome_message.decode('utf-8')}")

# Send messages to the server
while True:
    message = input("Enter a message for the server (or 'exit' to end): ")
    client_socket.sendall(message.encode('utf-8'))
    if message.lower() == 'exit':
        break

# Close the connection
client_socket.close()

