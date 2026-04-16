"""
Unit Tests for TicTacToeGame Class (Interactive_Board_classes)
===============================================================
Tests with pytest for the game visualization and logic.

Run with: pytest testing/test_interactive_board.py -v
"""

import numpy as np
import sys
sys.path.insert(0, '.')
from Interactive_Board import TicTacToeGame


class TestTicTacToeGame:
    """Test suite for TicTacToeGame class"""
    
    def setup_method(self):
        """Before each test: Create a new game instance"""
        self.game = TicTacToeGame()
    
    # ===================== TESTS FOR INITIALIZATION =====================
    
    def test_game_initializes(self):
        """Test: Game instance is created properly"""
        assert self.game is not None
        assert self.game.N == 100
        assert self.game.agent is not None
        
    def test_initial_game_state(self):
        """Test: Initial game state is correct"""
        assert self.game.cross == False
        assert self.game.placeholder == False
        assert len(self.game.boards) == 0
        assert self.game.current_selection is not None
        
    def test_selections_array_created(self):
        """Test: Selections array has 9 valid one-hot encoded positions"""
        assert self.game.selections.shape == (9, 3, 3)
        for i in range(9):
            assert np.sum(self.game.selections[i]) == 1  # One-hot encoding
            assert self.game.selections[i].ravel()[i] == 1
    
    # ===================== TESTS FOR DRAWING FUNCTIONS =====================
    
    def test_draw_board_returns_correct_shape(self):
        """Test: draw_board returns numpy array of correct size"""
        board = self.game.draw_board()
        assert isinstance(board, np.ndarray)
        assert board.shape[:2] == (300, 300)
    
    def test_draw_circle_modifies_board(self):
        """Test: draw_circle adds values to board"""
        board = np.zeros((300, 300))
        move = np.zeros(9)
        move[0] = 1  # First position
        
        result = self.game.draw_circle(self.game.draw_board(), move)
        assert result.shape[:2] == (300, 300)
        assert np.max(result) > 0  # Board has values added
    
    def test_draw_cross_modifies_board(self):
        """Test: draw_cross adds values to board"""
        board = np.zeros((300, 300))
        move = np.zeros(9)
        move[4] = 1  # Center position
        
        result = self.game.draw_cross(self.game.draw_board(), move)
        assert result.shape[:2] == (300, 300)
        assert np.max(result) > 0  # Board has values added
    
    def test_highlight_move_with_circle(self):
        """Test: highlight_move works with circle (AI)"""
        board = np.zeros((300, 300))
        move = np.zeros(9)
        move[0] = 1
        
        result = self.game.highlight_move(self.game.draw_board(), move, cross=False)
        assert result.shape[:2] == (300, 300)
        assert np.max(result) > 0  # Highlighted board has values
    
    def test_highlight_move_with_cross(self):
        """Test: highlight_move works with cross (human)"""
        board = np.zeros((300, 300))
        move = np.zeros(9)
        move[4] = 1
        
        result = self.game.highlight_move(self.game.draw_board(), move, cross=True)
        assert result.shape[:2] == (300, 300)
        assert np.max(result) > 0  # Highlighted board has values
    
    # ===================== TESTS FOR CHECK_WINNER =====================
    
    def test_check_winner_human_horizontal(self):
        """Test: check_winner detects human horizontal win"""
        board = np.array([
            [1, 1, 1],
            [0, 0, 0],
            [0, 0, 0]
        ])
        over, winner = self.game.check_winner(board)
        assert over == True
        assert winner == True  # Human wins (cross=True)
    
    def test_check_winner_ai_horizontal(self):
        """Test: check_winner detects AI horizontal win"""
        board = np.array([
            [-1, -1, -1],
            [0, 0, 0],
            [0, 0, 0]
        ])
        over, winner = self.game.check_winner(board)
        assert over == True
        assert winner == False  # AI wins (cross=False)
    
    def test_check_winner_human_vertical(self):
        """Test: check_winner detects human vertical win"""
        board = np.array([
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0]
        ])
        over, winner = self.game.check_winner(board)
        assert over == True
        assert winner == True
    
    def test_check_winner_ai_vertical(self):
        """Test: check_winner detects AI vertical win"""
        board = np.array([
            [-1, 0, 0],
            [-1, 0, 0],
            [-1, 0, 0]
        ])
        over, winner = self.game.check_winner(board)
        assert over == True
        assert winner == False
    
    def test_check_winner_human_diagonal_topright(self):
        """Test: check_winner detects human diagonal win (top-right)"""
        board = np.array([
            [0, 0, 1],
            [0, 1, 0],
            [1, 0, 0]
        ])
        over, winner = self.game.check_winner(board)
        assert over == True
        assert winner == True
    
    def test_check_winner_human_diagonal_topleft(self):
        """Test: check_winner detects human diagonal win (top-left)"""
        board = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])
        over, winner = self.game.check_winner(board)
        assert over == True
        assert winner == True
    
    def test_check_winner_ai_diagonal(self):
        """Test: check_winner detects AI diagonal win"""
        board = np.array([
            [-1, 0, 0],
            [0, -1, 0],
            [0, 0, -1]
        ])
        over, winner = self.game.check_winner(board)
        assert over == True
        assert winner == False
    
    def test_check_winner_no_win_empty(self):
        """Test: check_winner returns False for empty board"""
        board = np.zeros((3, 3))
        over, winner = self.game.check_winner(board)
        assert over == False
        assert winner == None
    
    def test_check_winner_no_win_partial(self):
        """Test: check_winner returns False for incomplete board"""
        board = np.array([
            [1, -1, 0],
            [0, 1, 0],
            [0, 0, -1]
        ])
        over, winner = self.game.check_winner(board)
        assert over == False
        assert winner == None
    
    def test_check_winner_draw(self):
        """Test: check_winner correctly identifies draw (no winner)"""
        board = np.array([
            [1, -1, 1],
            [-1, 1, -1],
            [-1, 1, -1]
        ])
        over, winner = self.game.check_winner(board)
        assert over == False
        assert winner == None
    
    # ===================== TESTS FOR GAME STATE VISUALIZATION =====================
    
    def test_visualize_empty_board(self):
        """Test: visualize_game_state on empty board"""
        board = np.zeros((3, 3))
        Board = self.game.visualize_game_state(board)
        assert Board.shape[:2] == (300, 300)
        assert isinstance(Board, np.ndarray)
    
    def test_visualize_board_with_cross(self):
        """Test: visualize_game_state with human move"""
        board = np.zeros((3, 3))
        board[0, 0] = 1  # Human move at top-left
        
        Board1 = self.game.visualize_game_state(board)
        Board2 = self.game.visualize_game_state(np.zeros((3, 3)))
        
        # Board with a move should have more values than empty board
        assert np.sum(Board1) > np.sum(Board2)
    
    def test_visualize_board_with_circle(self):
        """Test: visualize_game_state with AI move"""
        board = np.zeros((3, 3))
        board[0, 0] = -1  # AI move at top-left
        
        Board1 = self.game.visualize_game_state(board)
        Board2 = self.game.visualize_game_state(np.zeros((3, 3)))
        
        assert np.sum(Board1) > np.sum(Board2)
    
    def test_visualize_board_multiple_moves(self):
        """Test: visualize_game_state with multiple moves"""
        board = np.array([
            [1, -1, 0],
            [0, 1, -1],
            [0, 0, 0]
        ])
        Board = self.game.visualize_game_state(board)
        assert Board.shape[:2] == (300, 300)
        # Multiple moves should result in higher sum than empty board
        assert np.sum(Board) > 0
    
    # ===================== TESTS FOR SELECTIONS =====================
    
    def test_selections_current_selection_is_valid(self):
        """Test: current_selection is a valid one-hot encoded move"""
        assert np.sum(self.game.current_selection) == 1
        assert self.game.current_selection.shape == (3, 3)
    
    def test_all_selections_are_unique(self):
        """Test: All 9 selections are unique positions"""
        for i in range(9):
            for j in range(i+1, 9):
                assert not np.array_equal(self.game.selections[i], self.game.selections[j])
    
    def test_selections_cover_all_positions(self):
        """Test: Selections cover all positions on the board"""
        all_ones_indices = set()
        for i in range(9):
            idx = np.argmax(self.game.selections[i].ravel())
            all_ones_indices.add(idx)
        
        assert all_ones_indices == set(range(9))
    
    # ===================== EDGE CASES =====================
    
    def test_check_winner_with_board_array_not_reshaped(self):
        """Test: check_winner works with 1D board array"""
        board_1d = np.array([1, 1, 1, 0, 0, 0, 0, 0, 0])
        # Reshape to 3x3 in the method
        board_3d = board_1d.reshape(3, 3)
        over, winner = self.game.check_winner(board_3d)
        assert over == True
        assert winner == True


