import socket
import sys

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

		#all threads are stored in this list
		allthreads = list()
		
		#all users are stored in this list
		allusers = list()
		
		while True:
				data, addr = sock.recvfrom(1024) # (buffer size) 
				t = threading.Thread(name = data.split()[0],target=threading_function, args = (data, addr, sock, allusers,))
				allthreads.append((t, data, addr))
				t.start()
				
	except KeyboardInterrupt:
		
