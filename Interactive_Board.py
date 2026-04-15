####### we have to still make it possible to also have the ml code begin...
# also we could implement a random feature in the gto code, so it makes different moves everytime
# otherwise this runs nice...code could be made prettier though


from GTO_TTT import TicTacToeAI
import matplotlib.pyplot as plt
import numpy as np
import time 

agent = TicTacToeAI()
###### overall still some improvements to be made... however the grundgerüst steht...
###### still to do: implement the possibility of having either player start first
###### also: maybe make the code prettier

# Create the Board ### Not sure yet about the colors of the stripes...
def draw_board(ax, N):
    # Create Overall Board
    board_square = np.zeros((N,N))
    Board = np.kron(0.3*np.ones((3,3)), board_square)
    line = np.ones(3*N)
    # plotting the lines 
    ax.plot(N*line, np.linspace(0,3*N,3*N), color = 'gray')
    ax.plot(2*N*line, np.linspace(0,3*N,3*N),color = 'gray')
    ax.plot(np.linspace(0,3*N,3*N), N*line, color = 'gray')
    ax.plot(np.linspace(0,3*N,3*N), 2*N*line, color = 'gray')
    return Board

def draw_circle(Board, move,N, color = 0.3):
    # Create Circles
    circle = np.zeros((N,N))
    for i in range(N):
        for j in range(N):
            if ( (i-N/2)**2 + (j-N/2)**2) <= (N/4)**2 and ( (i-N/2)**2 + (j-N/2)**2) >= (N/5)**2:
                circle[i,j] = color
    Board += np.kron(move.reshape(3,3), circle)
    #plt.imshow(Board)
    #plt.show()
    return Board

def draw_cross(Board, move,N, color = 0.3):
    # Create Cross
    cross = np.zeros((N,N))
    for i in range(N):
        for j in range(N):
            if i == j and i > 10 and i < N-10:
                cross[i,j] = color
            if i == N-j and j > 10 and j < N-10:
                cross[i,j] = color
    Board += np.kron(move.reshape(3,3), cross)
    #plt.imshow(Board)
    #plt.show()
    return Board
    
def convert_board_to_Board(board, ax, N):
    # takes in a board with notation of 1's and -1's and vizualizes
    Board = draw_board(ax, N)
    move = np.zeros(9)
    for i in range(9):
        if board.ravel()[i] == 1:
            tmp_move = move.copy()
            tmp_move[i] = 1
            # ones are crosses
            Board = draw_cross(Board, tmp_move, N)
        elif board.ravel()[i] == -1:
            tmp_move = move.copy()
            tmp_move[i] = 1
            # twos are circles
            Board = draw_circle(Board, tmp_move, N)
    #plt.imshow(Board)
    return Board

def draw_move(Board, move, N, cross = False):
    # Vizualizes the Board + the new move
    # move has to be a numpy array
    if cross:
        Board = draw_cross(Board, move,N , 0.3)
    else:
        Board = draw_circle(Board, move,N , 0.3)
    Board += np.kron(move.reshape(3,3), 0.35*np.ones((N,N)))
    return Board

def un_draw_previous_move(Board, move, N, cross = False):
    # Vizualizes the Board + the new move
    # move has to be a numpy array
    if cross:
        tmp_Board = draw_cross(Board, move,N , 0.3)
    else:
        tmp_Board = draw_circle(Board, move,N , 0.3)
    Board -= np.kron(move.reshape(3,3), 0.35*np.ones((N,N))) 
    Board -= tmp_Board
    return Board

def winning_condition(board):
    #returns weather board is terminal, as well as the player, who has one
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
    # we need this global function to acess the current_selection variable
    #
    # in the following Board references the Matrix used to visualized, while board is the actual tictactoe board
    #
    #
    
    if placeholder:
        win, who = winning_condition(np.sum(boards, axis = 0))
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
        # we have to type N here explicitly... lets fix having to set it alltogether in the future
        for board in boards:
            Board += convert_board_to_Board(board, ax, N)
            
        if np.allclose(current_selection, selections[8]):
            idx = -1
        else:
            for i in range(8):
                if np.allclose(current_selection, selections[i]):
                    idx = i
        current_selection = selections[idx+1]   # resets the data for the move that is being considered
        Board += draw_move(Board, current_selection,N, cross)
        marker.set_data(Board) # resets the data for the point that we are plotting
        fig.canvas.draw_idle()
        # we need this draw_idle() function to make renewed plots
    elif event.key == 'left':
        Board = np.kron(np.identity(3), np.zeros((N,N)))
        for board in boards:
            Board += convert_board_to_Board(board, ax, N)
    
        for i in range(9):
            if np.allclose(current_selection, selections[i]):
                idx = i
        current_selection = selections[idx-1]
        Board += draw_move(Board, current_selection,N, cross)
        marker.set_data(Board)
        fig.canvas.draw_idle()
        
    elif event.key == 'enter':
        Board = np.kron(0.3*np.ones((3,3)), np.zeros((N,N)))
        for board in boards:
            Board += convert_board_to_Board(board, ax, N)
        # check, wheather space is occupied:
        move_index = np.argmax(current_selection.ravel())
        the_actual_board = np.zeros(9) + np.sum(boards, axis = 0).ravel()
        if the_actual_board[move_index] != 0:  
            print('That space is already taken!')

        else:
            Board += draw_move(Board, current_selection,N, cross)
            if cross:
                boards.append(current_selection )
            else:
                boards.append(current_selection * -1)
            win, who = winning_condition(np.sum(boards, axis = 0))
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
           

           # # # wir tricksen hier grad noch in dem ersten und zweiten zug, damit es schneller geht
            time.sleep(0.35)
           
            tmp_board = np.sum(boards, axis=0).ravel()
          
            if np.count_nonzero(tmp_board == 0) == 9: 
                move_index = np.random.randint(9)
            elif  np.count_nonzero(tmp_board == 0) == 8:
                if np.argmax(tmp_board.ravel()) == 4:
                    possible_moves = [1,0,1,0,0,0,1,0,1]
                    move_index = np.argsort(possible_moves-np.random.rand(9)/100)[-1]
                else:
                    move_index = 4 # this is the only move then :)
                    #move_index = np.argsort(np.sum(boards, axis = 0).ravel() - np.random.rand(9)/100)[0] # with this there is one way to beat him hehe
                   
            else:
                new_board = agent.gto(tmp_board, cross)[1]
                move_index = np.argmax(np.abs(new_board-tmp_board.ravel()))
                print(move_index)
            # print(move_index)
         
          
            # this was used prior to q_network:
            #np.argmin(np.sum(boards, axis=0).ravel()-np.random.rand(9)) # selects randomly one of the free spots
          
            current_selection = selections[move_index]
            #
            # here we have copied the same code from above... maybe we can make it shorter
            Board = draw_move(Board, current_selection,N, cross)
            if cross:
                boards.append(current_selection)
            else:
                boards.append(current_selection * -1)
          
          
            marker.set_data(Board)
            fig.canvas.draw_idle()
            cross = not cross
          
            win, who = winning_condition(np.sum(boards, axis = 0))
            if  who:
                placeholder = True


            print(np.sum(boards, axis=0))
# #Selections = Possible Moves in one array
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
alert = False
boards = []
draw_board(ax, N)

first_move = np.array([0,0,0,0,0,0,0,0,0])
first_move[np.random.randint(9)] = 1 
boards.append(first_move.reshape(3,3))

Board = convert_board_to_Board(current_selection, ax, N)
move = draw_move(Board, current_selection,N, cross = False)
marker = ax.imshow(move, cmap = 'gist_earth')


fig.canvas.mpl_connect('key_press_event', on_key)
plt.show()
