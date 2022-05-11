import json
import socket
import threading
import time
import random


class Tic_net_client():
	def __init__(self,port=12345):
		self.port=port
		#self.multicast_group="224.1.1.1"
		self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP
		self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		# Enable broadcasting mode
		self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		# Bind to the server address
		self.client.bind(('',port))
		self.client.settimeout(1.2)

		self.name="Laci"
		#in and outbox
		self.inbox=[]
		self.clients_avil={} # id name pairs
		self.id=0 #0 means it has not jet received an id
		self.stop=False
		
	def refresh_playes(self): # 200 milis
		remove_id=[]
		for id,user, in self.clients_avil.items():
			p,ttl=user
			ttl-=1
			self.clients_avil[id]=(p,ttl)
			if ttl<=0:
				remove_id.append(id)
		
		for id in remove_id:
			del self.clients_avil[id]

		#self.clients_avil={}
		self.send({"type":"WHO"})
		time.sleep(0.1)

	

	def send(self,obj,dest=0): # 0 is all
		if "type" not in obj.keys():
			obj["type"]="cmd"
		if self.id == 0:
			data = {"src": self.id, "dest": 0,"type":"WHO"}
			json_dump = json.dumps(data)
			sent = self.client.sendto(json_dump.encode(), ('<broadcast>',self.port))
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
		sent = self.client.sendto(json_dump.encode(),  ('<broadcast>',self.port))
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
				data, address = self.client.recvfrom(1024)
				#print(data)
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
					self.clients_avil[msg["id"]]=(msg["name"],10)
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
	print("receiver")
	tn=Tic_net_client()
	tn.Start()
	while True:
		msgs=tn.get_messages()
		for m in msgs:
			print(m)
			if m["dest"] != tn.id: # scip if its not sent to us
				continue
			if m["data"] == "CHALLENGE":
				data={"data":"ACCEPT"}
				#tn.gotack=False
				tn.send(data,m["src"])
			if m["data"] == "CANCEL" and m["src"]:
				pass
			if m["data"] == "ACCEPT" and m["src"]:
				pass
			if m["data"] == "STEP" and m["src"]:
				data={"data":"ACK","to":m["to"]}
				#tn.gotack=False
				tn.send(data,m["src"])
				data={"data":"STEP","to":random.randint(0,8)}
				tn.send(data,m["src"])
				pass
			if m["data"] == "ACK" and m["src"]:
				#self.gotack=True
				pass

		pass
