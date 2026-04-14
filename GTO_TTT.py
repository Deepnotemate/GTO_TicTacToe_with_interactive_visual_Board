import numpy as np

def winning_condition(board, player):
    board_numpy = np.array(board).reshape(3,3)
    a = np.array([1,1,1])
    if not player:
        a *= 2
    for i in range(3):
        if (board_numpy[i] == a).all() or (board_numpy.T[i] == a).all():
            return True
        elif (np.diag(board_numpy) == a).all() or (np.diag(np.fliplr(board_numpy)) == a).all():
            return True
    return False

def evaluate_move(board):
    if winning_condition(board,True):
        return 1
    elif winning_condition(board,False):
        return -1
    else:
        return 0
    
def find_zero_indices(board):
    zeros = []
    for i in range(9):
        if board[i] == 0:
            zeros.append(i)
    return zeros

def create_board(board, zero, player):
    boardcopy = board.copy()
    boardcopy[zero] =  (player)*-1 + 2
    return boardcopy

def newboards(board, player):
    newboards = []
    zeros = find_zero_indices(board)
    #newboards:
    for zero in zeros:
        newboards.append(create_board(board, zero, player))
    return newboards 

def gto(board, player):
    if winning_condition(board, False) or winning_condition(board, True) or np.count_nonzero(np.array(board)==0) == 0:
        return evaluate_move(board), board
    returns = []
    new_boards = newboards(board, player)
    for new in new_boards:
        returns.append(gto(new, not player)[0])
    if player:
        # index = returns.index(max(returns)) # we used to use this, but the following code provides random choices, if the returns are equal for different spaces
        index = np.argsort(np.array(returns)-np.random.rand(len(returns)))[-1]
    elif not player:
        # index = returns.index(min(returns)) 
        index = np.argsort(np.array(returns)-np.random.rand(len(returns)))[0]
    out_board = new_boards[index]
    return returns[index], out_board