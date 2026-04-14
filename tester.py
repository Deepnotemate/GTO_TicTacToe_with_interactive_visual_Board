import numpy as np
import matplotlib.pyplot as plt
from GTO_TTT import gto

board = [1,0,0,0,-1,1,0,0,0]
print(np.array(gto(board, False)[1]).reshape(3,3))
print()
board = [0,0,0,0,2,1,0,0,0]
print(np.array(gto(board, True)[1]).reshape(3,3))
print()
board = [1,-1,1,0,-1,1,0,0,0]
print(np.array(gto(board, False)[1]).reshape(3,3))
print()
board = [1,2,0,0,2,1,0,0,0]
print(np.array(gto(board, True)[1]).reshape(3,3))
print()


# tmp_board = np.array([1,2,0,0,2,1,0,0,0] )
# new_board = np.array(gto(tmp_board, True)[1])
# move_index = np.argmax(new_board-tmp_board.reshape(3,3).ravel())
# print(tmp_board.reshape(3,3))
# print(new_board.reshape(3,3))

# print(move_index)
# print()

# board = [-1,0,0,0,1,0,0,0,0]
# print(np.array(gto(board, False)[1]).reshape(3,3))
# print()

