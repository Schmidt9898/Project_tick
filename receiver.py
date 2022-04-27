import time
from server import Tic_net_client


print("receiver")









tn=Tic_net_client()
tn.Start()
while True:
	s=input()
	print(tn.get_new_id())
	tn.send(s)
	#time.sleep(1)






















#import socket
#import struct
#import time
#multicast_group = '224.1.1.1'
#port= 12345
#mg = (multicast_group,port)
## Create the socket
#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
## Bind to the server address
#sock.bind(('',port))
#
## Tell the operating system to add the socket to the multicast group
## on all interfaces.
#group = socket.inet_aton(multicast_group)
#mreq = struct.pack('4sL', group, socket.INADDR_ANY)
#sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
#
#sock.settimeout(5)
#data, address = sock.recvfrom(1024)
#sock.sendto("get_id".encode(), address)
## Receive/respond loop
#i=0;
#while True:
#	#print("nnnnnn ",i)
#	data, address = sock.recvfrom(1024)
#	print (address,"-",data)
#	msg = data.decode()
#	if i==0 and msg.__contains__("your_id:"):
#		msg=msg.split(':')[1]
#		print ("my id: ",msg)
#		i=int(msg)
#	
#	if i==1:
#		sock.sendto(("i am: "+str(i)).encode(), address)
#		time.sleep(3)
#	if i==2:
#		sock.sendto(("i am: "+str(i)).encode(), address)
#		time.sleep(1)
#	#i+=1
