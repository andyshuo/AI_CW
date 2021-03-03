from player import Player

import numpy as np

board = np.zeros((11,11), dtype=int)
agent = Player(-1,11,5)


board[0,5]=1
board[1,6]=1
board[2,7]=-1
board[3,8]=1
board[4,9]=1
#board[]=1
#board[]=1
#board[]=1
#board[]=1
#board[]=1
#board[]=1
#board[]=1
#board[]=1
print(board)

print(agent.evaluate_move(board))
