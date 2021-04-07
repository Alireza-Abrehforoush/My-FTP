import socket as sct
import os

server_name = "127.0.0.1"
server_port = 2121
client_socket = sct.socket(sct.AF_INET, sct.SOCK_DGRAM)
while True:
    command = input("Enter Command: ")
    client_socket.sendto(command.encode(), (server_name, server_port))
    answer, server_address = client_socket.recvfrom(2048)
    print(answer.decode())
    client_socket.close()