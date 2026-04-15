import numpy as np
import matplotlib.pyplot as plt
import time

from GTO_TTT import TicTacToeAI


class TicTacToeGame:
    def __init__(self):
        self.N = 100
        self.agent = TicTacToeAI()
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect('equal')
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        # Game state variables
        self.boards = []
        self.selections = np.zeros((9,3,3))
        for i in range(9):
            self.selections[i].ravel()[i] = 1
        self.current_selection = self.selections[0]
        self.cross = False
        self.placeholder = False
        self.marker = None
        
    def draw_board(self):
        # Create grid background
        board_square = np.zeros((self.N,self.N))
        Board = np.kron(0.3*np.ones((3,3)), board_square)
        line = np.ones(3*self.N)
        # Draw vertical and horizontal grid lines
        self.ax.plot(self.N*line, np.linspace(0,3*self.N,3*self.N), color = 'gray')
        self.ax.plot(2*self.N*line, np.linspace(0,3*self.N,3*self.N),color = 'gray')
        self.ax.plot(np.linspace(0,3*self.N,3*self.N), self.N*line, color = 'gray')
        self.ax.plot(np.linspace(0,3*self.N,3*self.N), 2*self.N*line, color = 'gray')
        return Board

    def draw_circle(self, Board, move, color = 0.3):
        # Draw AI player symbol (circle)
        circle = np.zeros((self.N,self.N))
        for i in range(self.N):
            for j in range(self.N):
                if ( (i-self.N/2)**2 + (j-self.N/2)**2) <= (self.N/4)**2 and ( (i-self.N/2)**2 + (j-self.N/2)**2) >= (self.N/5)**2:
                    circle[i,j] = color
        Board += np.kron(move.reshape(3,3), circle)
        return Board

    def draw_cross(self, Board, move, color = 0.3):
        # Draw human player symbol (X)
        cross = np.zeros((self.N,self.N))
        for i in range(self.N):
            for j in range(self.N):
                if i == j and i > 10 and i < self.N-10:
                    cross[i,j] = color
                if i == self.N-j and j > 10 and j < self.N-10:
                    cross[i,j] = color
        Board += np.kron(move.reshape(3,3), cross)
        return Board
        
    def visualize_game_state(self, board):
        # Convert board state to visual representation
        Board = self.draw_board()
        move = np.zeros(9)
        for i in range(9):
            if board.ravel()[i] == 1:
                tmp_move = move.copy()
                tmp_move[i] = 1
                Board = self.draw_cross(Board, tmp_move)
            elif board.ravel()[i] == -1:
                tmp_move = move.copy()
                tmp_move[i] = 1
                Board = self.draw_circle(Board, tmp_move)
        return Board

    def highlight_move(self, Board, move, cross = False):
        # Draw move with visual highlight overlay
        if cross:
            Board = self.draw_cross(Board, move, 0.3)
        else:
            Board = self.draw_circle(Board, move, 0.3)
        Board += np.kron(move.reshape(3,3), 0.35*np.ones((self.N,self.N)))
        return Board

    def check_winner(self, board):
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
        
    def on_key(self, event):
        if self.placeholder:
            win, who = self.check_winner(np.sum(self.boards, axis = 0))
            print(f'Player {int(who) +1} wins the game!')
            time.sleep(2)
            print('Thank You for playing!')
            time.sleep(1)
            plt.close('all')
        elif np.sum(np.sum(self.boards, axis = 0) == 0) == 0:
            print(' This is a Tie!')
            time.sleep(2)
            print('Thank You for playing!')
            time.sleep(1)
            plt.close('all')
        if event.key == 'right':
            Board = np.kron(np.identity(3), np.zeros((self.N,self.N)))
            for board in self.boards:
                Board += self.visualize_game_state(board)
                
            if np.allclose(self.current_selection, self.selections[8]):
                idx = -1
            else:
                for i in range(8):
                    if np.allclose(self.current_selection, self.selections[i]):
                        idx = i
            self.current_selection = self.selections[idx+1]
            Board += self.highlight_move(Board, self.current_selection, self.cross)
            self.marker.set_data(Board)
            self.fig.canvas.draw_idle()
        elif event.key == 'left':
            Board = np.kron(np.identity(3), np.zeros((self.N,self.N)))
            for board in self.boards:
                Board += self.visualize_game_state(board)
        
            for i in range(9):
                if np.allclose(self.current_selection, self.selections[i]):
                    idx = i
            self.current_selection = self.selections[idx-1]
            Board += self.highlight_move(Board, self.current_selection, self.cross)
            self.marker.set_data(Board)
            self.fig.canvas.draw_idle()
            
        elif event.key == 'enter':
            Board = np.kron(0.3*np.ones((3,3)), np.zeros((self.N,self.N)))
            for board in self.boards:
                Board += self.visualize_game_state(board)
            move_index = np.argmax(self.current_selection.ravel())
            current_board_state = np.zeros(9) + np.sum(self.boards, axis = 0).ravel()
            if current_board_state[move_index] != 0:
                print('That space is already taken!')

            else:
                Board += self.highlight_move(Board, self.current_selection, self.cross)
                if self.cross:
                    self.boards.append(self.current_selection )
                else:
                    self.boards.append(self.current_selection * -1)
                win, who = self.check_winner(np.sum(self.boards, axis = 0))
                if win:
                    print(f'Player {int(who) +1} wins the game!')
                    time.sleep(2)
                    print('Thank You for playing!')
                    time.sleep(1)
                    plt.close('all')
                elif np.sum(np.sum(self.boards, axis = 0) == 0) == 0:
                    print(' This is a Tie!')
                    time.sleep(2)
                    print('Thank You for playing!')
                    time.sleep(1)
                    plt.close('all')
                self.marker.set_data(Board)
                self.fig.canvas.draw_idle()
                self.cross = not self.cross
               
                time.sleep(0.35)
                tmp_board = np.sum(self.boards, axis=0).ravel()
                if np.count_nonzero(tmp_board == 0) == 9: 
                    move_index = np.random.randint(9)
                elif  np.count_nonzero(tmp_board == 0) == 8:
                    if np.argmax(tmp_board.ravel()) == 4:
                        possible_moves = [1,0,1,0,0,0,1,0,1]
                        move_index = np.argsort(possible_moves-np.random.rand(9)/100)[-1]
                    else:
                        move_index = 4
                else:
                    new_board = self.agent.gto(tmp_board, self.cross)[1]
                    move_index = np.argmax(np.abs(new_board-tmp_board.ravel()))
              
                self.current_selection = self.selections[move_index]
                Board = self.highlight_move(Board, self.current_selection, self.cross)
                if self.cross:
                    self.boards.append(self.current_selection)
                else:
                    self.boards.append(self.current_selection * -1)
              
                self.marker.set_data(Board)
                self.fig.canvas.draw_idle()
                self.cross = not self.cross
              
                win, who = self.check_winner(np.sum(self.boards, axis = 0))
                if  who:
                    self.placeholder = True

    def initialize_game(self):
        # Initialize game board
        self.draw_board()
        
        first_move = np.array([0,0,0,0,0,0,0,0,0])
        first_move[np.random.randint(9)] = 1 
        self.boards.append(first_move.reshape(3,3))
        
        Board = self.visualize_game_state(self.current_selection)
        move = self.highlight_move(Board, self.current_selection, cross = False)
        self.marker = self.ax.imshow(move, cmap = 'gist_earth')
        
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        
    def run(self):
        self.initialize_game()
        plt.show()


# Main execution
if __name__ == '__main__':
    game = TicTacToeGame()
    game.run()
