from threading import Thread
import socket

class Server(Thread):
	def __init__(self,port):
		Thread.__init__(self)
		self.isListening = True
		self.port = port

	def run(self):
		self.sock = socket.socket(socket.AF_INET,
                                  socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", self.port))
        self.sock.setblocking(0)
        self.sock.settimeout(5)

        while self.isListening():
        	try: 
        		data,address = self.sock.recvfrom(1024)
        		