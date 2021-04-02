import socket as sct

server_name = "127.0.0.1"
server_port = 2121
client_socket = sct.socket(AF_INET, SOCK_DGRAM)

valid_commands = ['HELP', 'LIST', 'DWLD', 'PWD', 'CD']
def helpClient():

while True:
    command = input("Input Your Command and Press Enter...")