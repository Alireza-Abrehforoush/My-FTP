import socket as sct
import os
server_port = 2121
server_socket = sct.socket(sct.AF_INET, sct.SOCK_DGRAM)
server_socket.bind(('127.0.0.1', server_port))

#functions
def ftpHelp():
    h = "Enter one of the following commands:\n\n    # HELP: 			    Show this help\n    # LIST: 			    List files\n    # DWLD \"file_path\": 	Download file\n    # PWD: 					Show current dir\n    # CD \"dir_name\": 		Change directory\n    # QUIT:					Exit\n"
    server_socket.sendto(h.encode(), client_address)

def ftpList():
    ls = ""
    files_folders = [f for f in os.listdir()]
    size_of_files_in_current_folder = 0
    for i in files_folders:
        if os.path.isdir(i):
            ls = ls + '>' + i + '(' + str(os.path.getsize(i)) + ' B)' + '\n'
        if os.path.isfile(i):
            ls = ls + ' ' + i + '(' + str(os.path.getsize(i)) + ' B)' + '\n'
            size_of_files_in_current_folder = size_of_files_in_current_folder + os.path.getsize(i)
    ls = ls + "\nTotal size of files in current directory: " + str(size_of_files_in_current_folder) + " Bytes\n"
    server_socket.sendto(ls.encode(), client_address)

while True:
    command, client_address = server_socket.recvfrom(2048)
    if command.decode() == "HELP":
        ftpHelp()

    elif command.decode() == "LIST":
        ftpList()