import numpy as np
import random

class Tictactoe():
    """Class for Tictactoe logic.

    .. note::

       This game is a 3x3 board with two players and it can
       save only the last three movements of every player.

    """
    def __init__(self):
        """Constructor of Tictactoe.

        It starts the plays of two players in self.marks
        and create the last movement variable self.mark
        """
        self.marks=[[],[]]
        #self.o=[]
        #self.x=[]
        #self.board_time=[0,0,0,0,0,0,0,0,0] #3x3
        self.mark=0# 0x 1 o

    def step(self,mark_,i):
        """Make a step in the board position i for a certain player

        :param mark_: mark of the player to play 0 = "x" and 1 ="o"
        :type name: int.
        :param i: position in the board array 0-8.
        :type name: int.
        :returns:  boolean -- If the movement is allowed and registered

        """
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

    def reset(self):
        """Reset the mark boards
        """
        self.marks=[[],[]]
        self.mark=0# 0x 1 o
        print("reset")

    @property
    def is_win(self):
        """Check if one player won
        :returns:  boolean -- If one of the players won. False= Player 0 won,
        True= Player 1 won, None = no one won yet.

        """
        for m in range(2):
            if len(self.marks[m])<3:
                continue
            o= self.marks[m].copy()
            o.sort()
            i = o[0]
            #check horizontal
            if i%3 == 0 and i+1 == o[1] and i+2 == o[2]:
                return m
            #check vertical
            if i/3 < 1 and i+3 == o[1] and i+6 == o[2]:
                return m
            #check diagonal
            if o==[0,4,8]:
                return m
            if o==[2,4,6]:
                return m
        return None



    def get_state(self):
        """Get board matrix as array
        :returns:  list -- array with board symbols with 8 elements, they
        can be "x" "o" or " "

        """
        state=[" "]*9
        mark=0
        for m in self.marks:
            for i in m:
                state[i]="x" if mark==0 else "o"
            mark=1
        return state

    def ai_player_move(self):
        """Make a movement in the board of the ai
        :returns:  boolean -- If the movement of the ai is allowed and registered

        """
        board  = self.get_state()
        # while self.step(1,random.randint(0, 8)):
        # 	pass
        possibleMoves = [x for x, symbol in enumerate(board) if symbol == ' ']
        #check if there is any winning move for ai after player to block
        for symbol in ["o","x"]:
            for i in possibleMoves:
                bc = board[:]
                bc[i] = symbol
                if ((bc[6] == symbol and bc[7] == symbol and bc[8] == symbol) or
                (bc[3] == symbol and bc[4] == symbol and bc[5] == symbol) or
                (bc[0] == symbol and bc[1] == symbol and bc[2] == symbol) or
                (bc[6] == symbol and bc[3] == symbol and bc[0] == symbol) or
                (bc[7] == symbol and bc[4] == symbol and bc[1] == symbol) or
                (bc[8] == symbol and bc[5] == symbol and bc[2] == symbol) or
                (bc[6] == symbol and bc[4] == symbol and bc[2] == symbol) or
                (bc[8] == symbol and bc[4] == symbol and bc[0] == symbol)):
                    move = i
                    return self.step(1,move)

        #try to put in the corner
        cornersOpen = []
        for i in possibleMoves:
            if i in [0,2,6,8]:
                cornersOpen.append(i)
        if len(cornersOpen) > 0:
            ln = len(cornersOpen)
            r = random.randrange(0, ln)
            return self.step(1,cornersOpen[r])

        #try to put in center
        if 5 in possibleMoves:
            move = 4
            return self.step(1,move)

        #try to put in edges
        edgesOpen = []
        for i in possibleMoves:
            if i in [1,3,5,7]:
                edgesOpen.append(i)

        if len(edgesOpen) > 0:
            ln = len(edgesOpen)
            r = random.randrange(0, ln)
            return self.step(1,edgesOpen[r])



def print3(s):
    """Print the board array as a matrix.
    """
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
        if g.is_win is not None:
            print("winner is ",g.is_win)
            break




