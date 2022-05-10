print("sender")

import json
import socket
import threading
import time
import random
import struct




class Tic_net_server():
	def __init__(self,port=12345):
		self.multicast_group=("224.1.1.1",port)
		self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.server.settimeout(1) ## message timeout
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
				#print ("Ping...")
				sent = self.server.sendto(b"{\"src\": 0, \"dest\": 0,\"type\":\"WHO\"}", self.multicast_group)

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

		self.client.settimeout(1.2)
		self.address=None

		self.name="Laci"
		#in and outbox
		self.inbox=[]
		self.clients_avil={} # id name pairs
		self.id=0 #0 means it has not jet received an id
		self.stop=False
		
	def refresh_playes(self): # 200 milis
		self.clients_avil={}
		self.send({"type":"WHO"})
		time.sleep(0.1)
		print("players",self.clients_avil)

	

	def send(self,obj,dest=0): # 0 is all
		#obj.id=self.id
		if "type" not in obj.keys():
			obj["type"]="cmd"
		#wait for server
		while self.address is None:
			print("waiting")
			time.sleep(0.1)
			pass
		if self.id == 0:
			data = {"src": self.id, "dest": 0,"type":"WHO"}
			json_dump = json.dumps(data)
			sent = self.client.sendto(json_dump.encode(), self.address)
			time.sleep(0.1)
			while True:
				r=random.randrange(1,100)
				if r not in self.clients_avil.keys():
					self.id=r
					print("my new id",r)
					break
		
		data = obj
		data["src"]=self.id
		data["dest"]=dest
		json_dump = json.dumps(data)
		#obj to json
		sent = self.client.sendto(json_dump.encode(), self.address)
		pass
	
	def get_messages(self):
		t=self.inbox
		#t=[msg for msg in self.inbox]
		self.inbox=[]
		return t

	def receiver_loop(self):
		print("receiver started")
		while not self.stop:
			try:
				data, self.address = self.client.recvfrom(1024)
				msg=data.decode()
				msg = json.loads(msg)
				if msg["src"] == self.id:
					continue

				if msg["type"] == "PING":
					continue

				#print(msg)
				if msg["type"] == "WHO":
					#print("-----i am sending my id")
					sent = self.send({"type":"IAM","id":self.id,"name":self.name})
				if msg["type"]=="IAM":
					self.clients_avil[msg["id"]]=msg["name"]
					#if msg["id"] not in self.clients_avil.keys()
				if msg["type"]=="cmd":
					self.inbox.append(msg)


					


			except Exception as e:
				#print("....",str(e))
				pass


	def Start(self):
		self.receiver_thread = threading.Thread(target=self.receiver_loop)
		self.receiver_thread.setDaemon(True)
		self.receiver_thread.start()
		self.send({"data":"init"})



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