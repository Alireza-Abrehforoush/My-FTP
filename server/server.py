
import socket as sct
import os
import random as rnd

print("Welcome to the FTP server\n")
print("To get started, connect to a client")
server_port = 2121
server_socket = sct.socket(sct.AF_INET, sct.SOCK_STREAM)
server_socket.bind(('127.0.0.1', server_port))

server_socket.listen(5)
print("Server listening on " + "0.0.0.0: " + str(server_port) + "\n")

os.chdir("files")
main_path = os.getcwd()

#functions
def getSizeOfDirectoriesIn(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


def ftpHelp(cnct_sock):
    print("Help ...")
    h = "Enter one of the following commands:\n\n    # HELP: 			    Show this help\n    # LIST: 			    List files\n    # DWLD \"file_path\": 	Download file\n    # PWD: 					Show current dir\n    # CD \"dir_name\": 		Change directory\n    # QUIT:					Exit\n"
    cnct_sock.send(h.encode())
    print("Help is sent\n")

def ftpList(cnct_sock):
    print("Listing files ...\n")
    ls = ""
    files_folders = [f for f in os.listdir()]
    size_of_files_in_current_folder = 0
    for i in files_folders:
        if os.path.isdir(i):
            ls = ls + '>' + '\t' + i + ' (' + str(getSizeOfDirectoriesIn(i)) + ' B)' + '\n'
            size_of_files_in_current_folder = size_of_files_in_current_folder + getSizeOfDirectoriesIn(i)
        if os.path.isfile(i):
            ls = ls + ' ' + '\t' + i + ' (' + str(os.path.getsize(i)) + ' B)' + '\n'
            size_of_files_in_current_folder = size_of_files_in_current_folder + os.path.getsize(i)
    ls = ls + "\nTotal directory size: " + str(size_of_files_in_current_folder) + " Bytes\n"
    cnct_sock.send(ls.encode())
    print("file listing sent successfully\n")

def ftpPwd(cnct_sock):
    print("pwd ...")
    current_path = os.getcwd()
    current_path = current_path + '\\'
    i = current_path.find("files")
    h = current_path[i+5:]
    cnct_sock.send(h.encode())
    print("Current directory sent\n")

def ftpDwld(file_path, cnct_sock):
    if os.path.isfile(file_path):
        if file_path.startswith(main_path) or (os.getcwd() + "\"" + file_path).startswith(main_path):
            print("Sending file...")
            data_port = rnd.randrange(3000, 50000)
            cnct_sock.send(str(data_port).encode())
            data_channel = sct.socket(sct.AF_INET, sct.SOCK_STREAM)
            data_channel.bind(("127.0.0.1", data_port))
            data_channel.listen(5)
            data_connection_socket, bddr = data_channel.accept()
            f = open(file_path, "rb")
            data_connection_socket.send(f.read())
            data_connection_socket.close()
            data_channel.close()
            print("File sent successfully\n")
        else:
            h = "You do not have permission to download this file!"
            cnct_sock.send(h.encode())
    else:
        k = "File not found"
        cnct_sock.send(k.encode())


def ftpCd(dir_name, cnct_sock):
    print("CD ...")
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
    cnct_sock.send(h.encode())
    print("New directory sent to client\n")


while True:
    connection_socket, addr = server_socket.accept()
    print("client " + "\"" + str(addr[0]) + "\"" + " connected to port: " + str(server_port))
    while True:
        command = connection_socket.recv(1024).decode()
        print("Recieved instruction: " + command)
        if command == "HELP" or command == "help":
            ftpHelp(connection_socket)

        elif command == "LIST" or command == "list":
            ftpList(connection_socket)

        elif command.startswith("DWLD") or command.startswith("dwld"):
            ftpDwld(command[5:], connection_socket)

        elif command == "PWD" or command == "pwd":
            ftpPwd(connection_socket)

        elif command.startswith("CD") or command.startswith("cd"):
            ftpCd(command[3:], connection_socket)

        elif command == "QUIT" or command == "quit":
            print("Exiting ...\n")
            break

        else:
            print("Invalid command")
            connection_socket.send("Invalid command entered\n".encode())
    server_socket.close()
    print("client " + "\"" + str(addr[0]) + "\"" + " disconnected:")