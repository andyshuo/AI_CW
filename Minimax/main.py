from player import Player

import numpy as np

board = np.zeros((11,11), dtype=int)
agent = Player(1,11,5)

board[5,5:8]=1
board[5,4]=-1


print(board)

print(agent.evaluate_move(board))
