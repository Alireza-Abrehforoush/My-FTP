
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

print("Sending server request")
print("Connected successfully\n\n")
print("Welcome to the FTP client\n")
server_name = "127.0.0.1"
server_port = 2121

client_socket = sct.socket(sct.AF_INET, sct.SOCK_STREAM)
client_socket.connect((server_name, server_port))

while True:
#    client_socket = sct.socket(sct.AF_INET, sct.SOCK_STREAM)
#    client_socket.connect((server_name, server_port))
    command = input("Enter Command: ")
    client_socket.send(command.encode())
    if not command.startswith("DWLD"):
        answer = client_socket.recv(1024)
        print(answer.decode())
#        client_socket.close()
    else:
        data_port = client_socket.recv(1024)
        recieveFile(int(data_port), command[5:])
