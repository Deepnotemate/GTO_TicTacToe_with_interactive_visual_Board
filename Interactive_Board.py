import numpy as np
import matplotlib.pyplot as plt
import time

from GTO_TTT import TicTacToeAI

# Create the Board
def draw_board(ax, N):
    # Create Overall Board
    board_square = np.zeros((N,N))
    Board = np.kron(0.3*np.ones((3,3)), board_square)
    line = np.ones(3*N)
    # Draw vertical and horizontal grid lines
    ax.plot(N*line, np.linspace(0,3*N,3*N), color = 'gray')
    ax.plot(2*N*line, np.linspace(0,3*N,3*N),color = 'gray')
    ax.plot(np.linspace(0,3*N,3*N), N*line, color = 'gray')
    ax.plot(np.linspace(0,3*N,3*N), 2*N*line, color = 'gray')
    return Board

def draw_circle(Board, move,N, color = 0.3):
    # Draw AI player symbol (circle)
    circle = np.zeros((N,N))
    for i in range(N):
        for j in range(N):
            if ( (i-N/2)**2 + (j-N/2)**2) <= (N/4)**2 and ( (i-N/2)**2 + (j-N/2)**2) >= (N/5)**2:
                circle[i,j] = color
    Board += np.kron(move.reshape(3,3), circle)
    return Board

def draw_cross(Board, move,N, color = 0.3):
    # Draw human player symbol (X)
    cross = np.zeros((N,N))
    for i in range(N):
        for j in range(N):
            if i == j and i > 10 and i < N-10:
                cross[i,j] = color
            if i == N-j and j > 10 and j < N-10:
                cross[i,j] = color
    Board += np.kron(move.reshape(3,3), cross)
    return Board
    
def visualize_game_state(board, ax, N):
    # Convert board state to visual representation
    Board = draw_board(ax, N)
    move = np.zeros(9)
    for i in range(9):
        if board.ravel()[i] == 1:
            tmp_move = move.copy()
            tmp_move[i] = 1
            Board = draw_cross(Board, tmp_move, N)
        elif board.ravel()[i] == -1:
            tmp_move = move.copy()
            tmp_move[i] = 1
            Board = draw_circle(Board, tmp_move, N)
    #plt.imshow(Board)
    #plt.show()
    return Board

def highlight_move(Board, move, N, cross = False):
    # Draw move with visual highlight overlay
    if cross:
        Board = draw_cross(Board, move,N , 0.3)
    else:
        Board = draw_circle(Board, move,N , 0.3)
    Board += np.kron(move.reshape(3,3), 0.35*np.ones((N,N)))
    return Board

def check_winner(board):
    # Check if game is won and return (is_terminal, winner)
    a = np.array([1,1,1])
    b = np.array([-1,-1,-1])
    for i in range(3):
        if (board[i] == a).all() or (board.T[i] == a).all():
            over = True
            cross = True
            return over, cross
        elif (board[i] == b).all() or (board.T[i] == b).all():
            over = True
            cross = False
            return over, cross
        elif (np.diag(board) == a).all() or (np.diag(np.fliplr(board)) == a).all():
            over = True
            cross = True
            return over, cross
        elif (np.diag(board) == b).all() or (np.diag(np.fliplr(board)) == b).all():
            over = True
            cross = False
            return over, cross
    return False, None
    
def on_key(event):
    global current_selection
    global cross
    global placeholder
    
    if placeholder:
        win, who = check_winner(np.sum(boards, axis = 0))
        print(f'Player {int(who) +1} wins the game!')
        time.sleep(2)
        print('Thank You for playing!')
        time.sleep(1)
        
        plt.close('all')
    elif np.sum(np.sum(boards, axis = 0) == 0) == 0:
        print(' This is a Tie!')
        time.sleep(2)
        print('Thank You for playing!')
        time.sleep(1)
        plt.close('all')
    if event.key == 'right':
        Board = np.kron(np.identity(3), np.zeros((N,N)))
        for board in boards:
            Board += visualize_game_state(board, ax, N)
            
        if np.allclose(current_selection, selections[8]):
            idx = -1
        else:
            for i in range(8):
                if np.allclose(current_selection, selections[i]):
                    idx = i
        current_selection = selections[idx+1]
        Board += highlight_move(Board, current_selection,N, cross)
        marker.set_data(Board)
        fig.canvas.draw_idle()
    elif event.key == 'left':
        Board = np.kron(np.identity(3), np.zeros((N,N)))
        for board in boards:
            Board += visualize_game_state(board, ax, N)
    
        for i in range(9):
            if np.allclose(current_selection, selections[i]):
                idx = i
        current_selection = selections[idx-1]
        Board += highlight_move(Board, current_selection,N, cross)
        marker.set_data(Board)
        fig.canvas.draw_idle()
        
    elif event.key == 'enter':
        Board = np.kron(0.3*np.ones((3,3)), np.zeros((N,N)))
        for board in boards:
            Board += visualize_game_state(board, ax, N)
        move_index = np.argmax(current_selection.ravel())
        current_board_state = np.zeros(9) + np.sum(boards, axis = 0).ravel()
        if current_board_state[move_index] != 0:
            print('That space is already taken!')

        else:
            Board += highlight_move(Board, current_selection,N, cross)
            if cross:
                boards.append(current_selection )
            else:
                boards.append(current_selection * -1)
            win, who = check_winner(np.sum(boards, axis = 0))
            if win:
                print(f'Player {int(who) +1} wins the game!')
                time.sleep(2)
                print('Thank You for playing!')
                time.sleep(1)
                
                plt.close('all')
            elif np.sum(np.sum(boards, axis = 0) == 0) == 0:
                print(' This is a Tie!')
                time.sleep(2)
                print('Thank You for playing!')
                time.sleep(1)
                plt.close('all')
            marker.set_data(Board)
            fig.canvas.draw_idle()
            cross = not cross
           
            time.sleep(0.35)
            tmp_board = np.sum(boards, axis=0).ravel()
            if np.count_nonzero(tmp_board == 0) == 9: 
                move_index = np.random.randint(9)
            elif  np.count_nonzero(tmp_board == 0) == 8:
                if np.argmax(tmp_board.ravel()) == 4:
                    possible_moves = [1,0,1,0,0,0,1,0,1]
                    move_index = np.argsort(possible_moves-np.random.rand(9)/100)[-1]
                else:
                    move_index = 4
            else:
                new_board = agent.gto(tmp_board, cross)[1]
                move_index = np.argmax(np.abs(new_board-tmp_board.ravel()))
          
            current_selection = selections[move_index]
            Board = highlight_move(Board, current_selection,N, cross)
            if cross:
                boards.append(current_selection)
            else:
                boards.append(current_selection * -1)
          
            marker.set_data(Board)
            fig.canvas.draw_idle()
            cross = not cross
          
            win, who = check_winner(np.sum(boards, axis = 0))
            if  who:
                placeholder = True

selections = np.zeros((9,3,3))
for i in range(9):
    selections[i].ravel()[i] = 1
current_selection = selections[0]

fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.set_xticks([])
ax.set_yticks([])
N = 100

placeholder = False
cross = False
boards = []
agent = TicTacToeAI()
draw_board(ax, N)

first_move = np.array([0,0,0,0,0,0,0,0,0])
first_move[np.random.randint(9)] = 1 
boards.append(first_move.reshape(3,3))


Board = visualize_game_state(current_selection, ax, N)

move = highlight_move(Board, current_selection,N, cross = False)
marker = ax.imshow(move, cmap = 'gist_earth')

fig.canvas.mpl_connect('key_press_event', on_key)
plt.show()
