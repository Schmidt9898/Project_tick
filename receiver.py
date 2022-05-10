import time
from server import Tic_net_client


print("receiver")

tn=Tic_net_client()
tn.Start()
tn.send({"data":"helo"})
while True:
	s=input()
	if s == "get":
		tn.refresh_playes()
	elif s == "in":
		print(tn.inbox)
	else:
		tn.send({"data":s})
		print(tn.clients_avil)
	#print(tn.get_new_id())
	#time.sleep(1)