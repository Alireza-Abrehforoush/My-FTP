import socket as sct
import os

server_port = 2121
server_socket = sct.socket(sct.AF_INET, sct.SOCK_DGRAM)
server_socket.bind(('127.0.0.1', server_port))

main_path = os.getcwd()
print(main_path)
#functions
def ftpHelp():
    print("Help ...")
    h = "Enter one of the following commands:\n\n    # HELP: 			    Show this help\n    # LIST: 			    List files\n    # DWLD \"file_path\": 	Download file\n    # PWD: 					Show current dir\n    # CD \"dir_name\": 		Change directory\n    # QUIT:					Exit\n"
    server_socket.sendto(h.encode(), client_address)

def ftpList():
    print("Listing files ...\n")
    ls = ""
    files_folders = [f for f in os.listdir()]
    size_of_files_in_current_folder = 0
    for i in files_folders:
        if os.path.isdir(i):
            ls = ls + '>' + i + ' (' + str(os.path.getsize(i)) + ' B)' + '\n'
        if os.path.isfile(i):
            ls = ls + ' ' + i + ' (' + str(os.path.getsize(i)) + ' B)' + '\n'
            size_of_files_in_current_folder = size_of_files_in_current_folder + os.path.getsize(i)
    ls = ls + "\nTotal size of files in current directory: " + str(size_of_files_in_current_folder) + " Bytes\n"
    server_socket.sendto(ls.encode(), client_address)

def ftpPwd():
    print("pwd ...")
    current_path = os.getcwd()
    current_path = current_path + '\\'
    i = current_path.find("server")
    h = current_path[i+6:]
    server_socket.sendto(h.encode(), client_address)

def ftpDwld(file_path):
    

def ftpCd(dir_name):
    print("CD")
    previous_path = os.getcwd()
    if os.path.isdir(dir_name):
        os.chdir(dir_name)
        if not os.getcwd().startswith(main_path):
            os.chdir(previous_path)
            h = "You are not permitted to access this path\n"
        else:
            h = "Directory changed\n"
    else:
        h = "Directory " + '\"' + dir_name + '\"' + " not found!\n"
    print("Current Directory is set to" + " \"" + os.getcwd() + "\"")
    server_socket.sendto(h.encode(), client_address)
    print("New directory sent to client\n")



while True:
    command, client_address = server_socket.recvfrom(2048)
    print("Recieved instruction: " + command.decode())
    if command.decode() == "HELP":
        ftpHelp()

    elif command.decode() == "LIST":
        ftpList()

    elif command.decode().startswith("DWLD"):


    elif command.decode() == "PWD":
        ftpPwd()

    elif command.decode().startswith("CD"):
        ftpCd(command.decode()[3:])

    elif command.decode() == "QUIT":
        break

    else:
        continue