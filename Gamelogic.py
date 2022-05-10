import numpy as np
import random

class Tictactoe():
	def __init__(self):
		self.marks=[[],[]]
		#self.o=[]
		#self.x=[]
		#self.board_time=[0,0,0,0,0,0,0,0,0] #3x3
		self.mark=0# 0x 1 o
		self.turn=[True,False]
		self.is_end = False
		self.who_won = None

	def step(self,mark_,i):
		if self.is_end is False:
			if self.turn[mark_]:
				if self.mark != mark_:
					#print(mark_," can't step")
					return
				if i in self.marks[0] or i in self.marks[1]:
					#print(i," is taken.")
					return
				if len(self.marks[mark_])>2:
					self.marks[mark_].pop(0)
				self.marks[mark_].append(i)
				self.mark = (self.mark+1) % 2
				if mark_==0:
					self.turn[1]=True
					self.turn[0]=False
				else:
					self.turn[1]=False
					self.turn[0]=True
			#else:
				#print(mark_," can't step")
			self.check_is_win()

	def check_is_win(self):
		#check rows
		matrix = self.get_matrix_state()
		for row in matrix:
			if row.count("x")==3:
				self.is_end = True
				self.who_won = 0
			if row.count("o")==3:
				self.is_end = True
				self.who_won = 1
		#check cols
		for i in range(3):
			col = []
			for j in range(3):
				col.append(matrix[j][i])
			if col.count("x")==3:
				self.is_end = True
				self.who_won = 0
			if col.count("o")==3:
				self.is_end = True
				self.who_won = 1

		diagonal_row1 = [matrix[0][0],matrix[1][1],matrix[2][2]]
		if diagonal_row1.count("x")==3:
				self.is_end = True
				self.who_won = 0
		if diagonal_row1.count("o")==3:
			self.is_end = True
			self.who_won = 1

		diagonal_row2 = [matrix[0][2],matrix[1][1],matrix[0][2]]
		if diagonal_row2.count("x")==3:
				self.is_end = True
				self.who_won = 0
		if diagonal_row2.count("o")==3:
			self.is_end = True
			self.who_won = 1


	def get_state(self):
		state=[" "]*9
		mark=0
		for player in range(len(self.marks)):
			for i in self.marks[player]:
				if player == 0:
					state[i]="x"
				else:
					state[i]="o"
		return state

	def get_matrix_state(self):
		matrix = []
		for i in range(3):
			row = []
			for j in range(3):
				mark_in=0
				for player in range(len(self.marks)):
					if i*3+j in self.marks[player]:
						if player == 0:
							row.append("x")
							mark_in=1
						else:
							row.append("o")
							mark_in=1
				if not mark_in:
					row.append(" ")
			matrix.append(row)
		return matrix

	def ai_player_move(self):
		matrix = self.get_matrix_state()
		#print(matrix)
		#first if there is 3 empty spaces
		for i in range(len(matrix)):
			empty_spaces = matrix[i].count(" ")
			if empty_spaces == 3:
				self.step(1,3*i+random.randint(0, 2))
				return
		#first if there is 2 empty spaces
		for i in range(len(matrix)):
			empty_spaces = matrix[i].count(" ")
			if empty_spaces == 2:
				for j in range(3):
					rand_number = random.randint(0, 2)
					if matrix[i][rand_number] == " ":
						self.step(1,3*i+rand_number)
						return

		#first if there is 2 empty spaces
		for i in range(len(matrix)):
			empty_spaces = matrix[i].count(" ")
			if empty_spaces == 1:
				for j in range(3):
					rand_number = random.randint(0, 1)
					if matrix[i][rand_number] == " ":
						self.step(1,3*i+rand_number)
						return





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
		if g.is_win() is not None:
			print("winner is ",g.is_win())
			break




