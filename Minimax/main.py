from player import Player

import numpy as np

board = np.zeros((11,11), dtype=int)
agent = Player(-1,11,5)



#board[2,3]=-1
board[2,4]=-1
board[3,5]=1
board[3,7]=-1
board[4,5]=-1
board[4,6]=1
board[5,5]=1
board[5,6]=-1
board[5,7]=1
board[6,8]=1
board[7,9]=-1
board[8,10]=1

print(board)

print(agent.evaluate_move(board))
#a = np.array([1])
#b = np.array([1,1,1,1,1])
#compare = a==b
#print(compare.all())