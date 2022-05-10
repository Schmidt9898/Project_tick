import numpy as np

class Tictactoe():
	def __init__(self):
		self.marks=[[],[]]
		#self.o=[]
		#self.x=[]
		#self.board_time=[0,0,0,0,0,0,0,0,0] #3x3
		self.mark=0# 0x 1 o

	def step(self,mark_,i):
		if self.mark != mark_:
			print(mark_," can't step")
			return False
		if i in self.marks[0] or i in self.marks[1]:
			print(i," is taken.")
			return False
		if len(self.marks[mark_])>2:
			self.marks[mark_].pop(0)
		self.marks[mark_].append(i)
		self.mark = (self.mark+1) % 2
		return True

	def is_win(self):
		#test X
		##if len(self.o)<3 or len(self.x)<3:
		##	return None

		for m in range(2):
			if len(self.marks[m])<3:
				continue
			o= self.marks[m].copy()
			o.sort()
			i = o[0]
			#check horizontal
			if i+1 == o[1] and i+2 == o[2]:
				return m
			#check vertical
			if i+3 == o[1] and i+6 == o[2]:
				return m
			#check diagonal
			if o==[0,4,8]:
				return m
			if o==[2,4,6]:
				return m
		return None




	def get_state(self):
		state=[" "]*9
		mark=0
		for m in self.marks:
			for i in m:
				state[i]="x" if mark==0 else "o"
			mark=1
		return state


def print3(s):
	B = np.reshape(s, (3, 3))
	print(B)

if __name__ == "__main__":
	g=Tictactoe()
	#g.stepx(2)
	#g.stepx(2)
	#g.stepo(1)
	#g.stepo(1)
#
	#g.stepx(2)
	#g.stepx(5)
	#g.stepo(4)
#
	#print3(g.get_state())
	#print("-"*30)
	#g.stepx(0)
	#g.stepo(3)
	#print3(g.get_state())
	#g.stepx(8)
	#g.stepo(7)
	#

	while True:
		step=int(input())
		print("\n"*20)
		print(step)
		g.step(0,step)
		g.step(1,step)
		#g.stepo(step)
		print3(g.get_state())
		if g.check_is_win() is not None:
			print("winner is ",g.is_win())
			break




