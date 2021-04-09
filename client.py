
import socket as sct
import os

#functions
def recieveFile(port, file_name):
    data_channel = sct.socket(sct.AF_INET, sct.SOCK_STREAM)
    try:
        data_channel.connect(("127.0.0.1", port))
    except:
        return False
    data = b""
    while True:
        temp = data_channel.recv(1024)
        data = data + temp
        if not temp:
            break
    f = open(file_name, "wb")
    f.write(data)
    data_channel.close()
    return True



server_name = "127.0.0.1"
server_port = 2121

print("Sending server request")
client_socket = sct.socket(sct.AF_INET, sct.SOCK_STREAM)
client_socket.connect((server_name, server_port))
print("Connected successfully\n\n")
print("Welcome to the FTP client\n")
print("Enter one of the following commands:\n\n    # HELP: 			    Show this help\n    # LIST: 			    List files\n    # DWLD \"file_path\": 	Download file\n    # PWD: 					Show current dir\n    # CD \"dir_name\": 		Change directory\n    # QUIT:					Exit\n")
while True:
    command = input("Enter Command: ")
    client_socket.send(command.encode())
    if not command.startswith("DWLD"):
        answer = client_socket.recv(1024)
        print(answer.decode())
    else:
        data_port = client_socket.recv(1024)
        recieveFile(int(data_port), command[5:])
