import socket
import sys

client1 = ""
client2 = ""

if __name__ == "__main__":

	try:
		#checking for correct usage
		if len(sys.argv) < 3:
			print("python3 server.py –p <portNumber>")
			sys.exit()

		#collecting info from command line
		UDP_IP = "127.0.0.1"
		UDP_PORT = int(sys.argv[2])
			
		#creating socket 
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # (Internet, UDP)
		sock.bind((UDP_IP, UDP_PORT))
		
		print("server started on 127.0.0.1 at port "+ str(UDP_PORT))
		
		#initializing two clients
		data, addr = sock.recvfrom(1024) #receive from first client 
		if data == "register".encode():
			client1 = addr
			sock.sendto("1".encode(), client1)
			print("Client 1 has connected from " + addr[0] + ", " + str(addr[1]))
			
		data, addr = sock.recvfrom(1024) #receive from second client 
		if data == "register".encode():
			client2 = addr
			sock.sendto("2".encode(), client2)
			print("Client 2 has connected from " + addr[0] + ", " + str(addr[1]))
			
		while True:
			data, addr = sock.recvfrom(1024)
			
			if addr[1] == client1[1]:
				sock.sendto(data, client2)
				print("Client 1: " + data.decode("utf-8"))
			else:
				sock.sendto(data, client1)
				print("Client 2: " + data.decode("utf-8"))
	except KeyboardInterrupt:
		sys.exit()