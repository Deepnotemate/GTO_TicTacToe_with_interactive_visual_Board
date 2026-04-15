import numpy as np


class TicTacToeAI:
    """Game Theory Optimal AI for Tic Tac Toe using minimax algorithm."""
    
    # Constants for player representation
    HUMAN = 1
    AI = -1
    EMPTY = 0
    
    def __init__(self):
        pass
    
    def _get_player_mark(self, is_human):
        """Get the mark for a player (1 for human, -1 for AI)."""
        return self.HUMAN if is_human else self.AI
    
    def _check_line(self, line, target):
        """Check if a line matches the target pattern."""
        return (line == target).all()
    
    def check_winning_condition(self, board, is_human):
        """Check if a player has won.
        
        Args:
            board: List of 9 values (0, 1, -1)
            is_human: True for human, False for AI
        
        Returns:
            True if player has won, False otherwise
        """
        board_array = np.array(board).reshape(3, 3)
        target = np.array([self._get_player_mark(is_human)] * 3)
        
        # Check rows and columns
        for i in range(3):
            if self._check_line(board_array[i], target) or self._check_line(board_array.T[i], target):
                return True
        
        # Check diagonals
        if self._check_line(np.diag(board_array), target) or self._check_line(np.diag(np.fliplr(board_array)), target):
            return True
        
        return False
    
    def evaluate_move(self, board):
        """Score the current board state.
        
        Returns:
            1 if human won, -1 if AI won, 0 if draw/ongoing
        """
        if self.check_winning_condition(board, True):
            return 1
        elif self.check_winning_condition(board, False):
            return -1
        else:
            return 0
    
    def find_empty_cells(self, board):
        """Find all empty cells on the board.
        
        Returns:
            List of indices where board[i] == 0
        """
        return [i for i in range(9) if board[i] == self.EMPTY]
    
    def place_move(self, board, position, is_human):
        """Create a new board with a move placed.
        
        Args:
            board: Current board state
            position: Index of empty cell to fill
            is_human: True for human move, False for AI move
        
        Returns:
            New board with move placed
        """
        board_copy = board.copy()
        board_copy[position] = self._get_player_mark(is_human)
        return board_copy
    
    def get_possible_boards(self, board, is_human):
        """Generate all possible next board states.
        
        Args:
            board: Current board state
            is_human: Whose turn it is
        
        Returns:
            List of all possible boards after placing a move
        """
        empty_cells = self.find_empty_cells(board)
        return [self.place_move(board, pos, is_human) for pos in empty_cells]
    
    def _is_game_over(self, board):
        """Check if the game has ended."""
        human_won = self.check_winning_condition(board, True)
        ai_won = self.check_winning_condition(board, False)
        board_full = len(self.find_empty_cells(board)) == 0
        return human_won or ai_won or board_full
    
    def gto(self, board, is_human):
        """Game Theory Optimal move using minimax algorithm.
        
        Args:
            board: Current board state
            is_human: True for human's turn, False for AI's turn
        
        Returns:
            Tuple of (best_score, best_board)
        """
        # Base case: game over
        if self._is_game_over(board):
            return self.evaluate_move(board), board
        
        # Recursive case: evaluate all possible moves
        possible_boards = self.get_possible_boards(board, is_human)
        move_scores = [self.gto(board_state, not is_human)[0] for board_state in possible_boards]
        
        # Choose best move: maximize if human, minimize if AI
        best_index = np.argmax(move_scores) if is_human else np.argmin(move_scores)
        best_board = possible_boards[best_index]
        
        return move_scores[best_index], best_board
    
    def get_best_move(self, board):
        """Get the best move for the AI.
        
        Args:
            board: Current board state (as numpy array or list)
        
        Returns:
            Best board state after AI's move
        """
        _, best_board = self.gto(board, is_human=False)
        return best_board
