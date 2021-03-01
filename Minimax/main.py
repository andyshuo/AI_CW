from player import Player

import numpy as np

board = np.zeros((11,11), dtype=int)
agent = Player(1,11,5)

board[5,5:9]=1

print(board)

print(agent.evaluate_move(board,5,4))
