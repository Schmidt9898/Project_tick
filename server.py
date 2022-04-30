print("sender")

import socket
import threading
import time
import random
import struct


class Tic_net_server():
	def __init__(self,port=12345):
		self.multicast_group=("224.1.1.1",port)
		self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.server.settimeout(5) ## message timeout
		ttl = 2
		self.server.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

		self.id_counter=1
	
	def Start(self):
		sent = self.server.sendto(b"message", self.multicast_group)
		print("sent= ", sent)
		while True:
			try:
				data, address = self.server.recvfrom(1024)
				msg = data.decode()
				print (data)
				if msg == "PONG":
					continue
				#	print ("add id")
				#	sent = self.server.sendto(("your_id:"+str(self.id_counter)).encode(),self.multicast_group)
				#	self.id_counter+=1
				#else:
				sent = self.server.sendto(data, self.multicast_group)
			except:
				print ("Ping...")
				sent = self.server.sendto(b"PING", self.multicast_group)

	#time.sleep(1)


class Tic_net_client():
	def __init__(self,port=12345):
		self.multicast_group="224.1.1.1"
		self.client= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.client.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		# Bind to the server address
		self.client.bind(('',port))

		# Tell the operating system to add the socket to the multicast group
		# on all interfaces.
		group = socket.inet_aton(self.multicast_group)
		mreq = struct.pack('4sL', group, socket.INADDR_ANY)
		self.client.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

		self.client.settimeout(1)
		self.address=None
		#in and outbox
		self.inbox=[]
		self.clients_avil=[]
		self.id=0 #0 means it has not jet received an id
		self.stop=False
		
	def get_new_id(self): # 200 milis
		self.clients_avil=[]
		self.send("WHO")
		time.sleep(0.1)
		while True:
			r=random.randrange(1,100)
			if r not in self.clients_avil:
				self.id=r
				break
		return r
	
	def send(self,obj):
		#obj.id=self.id
		#obj to json
		sent = self.client.sendto(obj.encode(), self.address)
		pass
	
	def get_messages(self):
		t=[msg for msg in self.inbox] # convert to obj from json
		self.inbox=[]
		return t

	def receiver_loop(self):
		print("receiver started")
		while not self.stop:
			try:
				data, self.address = self.client.recvfrom(1024)
				msg=data.decode()
				print(msg)

				if msg == "PING":
					pass
				if msg == "WHO":
					sent = self.client.sendto(("IAM:"+str(self.id)).encode(), self.address)
				if msg.__contains__("IAM:"):
					self.clients_avil.append(int(msg.split(':')[1]))
				

					


				self.inbox.append(msg)
			except:
				pass		






	def Start(self):
		
		self.receiver_thread = threading.Thread(target=self.receiver_loop)
		self.receiver_thread.setDaemon(True)
		self.receiver_thread.start()



if __name__ == "__main__":
	tn=Tic_net_server()
	tn.Start()
	




























#
#
#
#message = 'very important data'
#multicast_group = ('224.1.1.1', 10000)
#
## Create the datagram socket
#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#
## Set a timeout so the socket does not block indefinitely when trying
## to receive data.
#sock.settimeout(2)
#
## Set the time-to-live for messages to 1 so they do not go past the
## local network segment.
#ttl = 2
#sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
#
#
#sent = sock.sendto(b"message", multicast_group)
#
#while True:
#	try:
#		data, address = sock.recvfrom(1024)
#		print (address,"\n",data)
#		sent = sock.sendto(data, multicast_group)
#	except:
#		print ("Ping...")
#		sent = sock.sendto(b"PING", multicast_group)
#
#	#time.sleep(1)