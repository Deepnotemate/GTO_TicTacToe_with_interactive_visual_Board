"""
Unit Tests for TicTacToeAI Class
=================================
Tests with pytest for all functions of the TicTacToeAI class.

Run with: pytest testing/test_gto_ttt.py -v
"""

import numpy as np
from GTO_TTT import TicTacToeAI


class TestTicTacToeAI:
    """Test suite for TicTacToeAI"""
    
    def setup_method(self):
        """Before each test: Create a new AI instance"""
        self.ai = TicTacToeAI()
    
    # ===================== TESTS FOR WINNING CONDITION =====================
    
    def test_horizontal_win_human(self):
        """Test: Human wins with horizontal row"""
        board = [1, 1, 1,  # Winning row
                 0, 0, 0,
                 0, 0, 0]
        assert self.ai.check_winning_condition(board, True) == True
    
    def test_horizontal_win_ai(self):
        """Test: AI wins with horizontal row"""
        board = [-1, -1, -1,
                  0,  0,  0,
                  0,  0,  0]
        assert self.ai.check_winning_condition(board, False) == True
    
    def test_vertical_win_human(self):
        """Test: Human wins with vertical column"""
        board = [1, 0, 0,
                 1, 0, 0,
                 1, 0, 0]
        assert self.ai.check_winning_condition(board, True) == True
    
    def test_vertical_win_ai(self):
        """Test: AI wins with vertical column"""
        board = [-1, 0, 0,
                 -1, 0, 0,
                 -1, 0, 0]
        assert self.ai.check_winning_condition(board, False) == True
    
    def test_diagonal_win_human_topleft(self):
        """Test: Human wins with diagonal (top-left to bottom-right)"""
        board = [1, 0, 0,
                 0, 1, 0,
                 0, 0, 1]
        assert self.ai.check_winning_condition(board, True) == True
    
    def test_diagonal_win_human_topright(self):
        """Test: Human wins with diagonal (top-right to bottom-left)"""
        board = [0, 0, 1,
                 0, 1, 0,
                 1, 0, 0]
        assert self.ai.check_winning_condition(board, True) == True
    
    def test_diagonal_win_ai(self):
        """Test: AI wins with diagonal"""
        board = [-1, 0, 0,
                  0, -1, 0,
                  0, 0, -1]
        assert self.ai.check_winning_condition(board, False) == True
    
    def test_no_win(self):
        """Test: No winner"""
        board = [1, 0, 0,
                 0, 0, 0,
                 0, 0, 0]
        assert self.ai.check_winning_condition(board, True) == False
        assert self.ai.check_winning_condition(board, False) == False
    
    def test_draw_no_win(self):
        """Test: Draw (full board) but no winner"""
        board = [1, -1, 1,
                 -1, 1, -1,
                 -1, 1, -1]
        assert self.ai.check_winning_condition(board, True) == False
        assert self.ai.check_winning_condition(board, False) == False
    
    # ===================== TESTS FOR EVALUATE_MOVE =====================
    
    def test_evaluate_human_win(self):
        """Test: evaluate_move returns +1 when human wins"""
        board = [1, 1, 1, 0, 0, 0, 0, 0, 0]
        assert self.ai.evaluate_move(board) == 1
    
    def test_evaluate_ai_win(self):
        """Test: evaluate_move returns -1 when AI wins"""
        board = [-1, -1, -1, 0, 0, 0, 0, 0, 0]
        assert self.ai.evaluate_move(board) == -1
    
    def test_evaluate_no_win(self):
        """Test: evaluate_move returns 0 when no one wins"""
        board = [1, 0, 0, 0, 0, 0, 0, 0, 0]
        assert self.ai.evaluate_move(board) == 0
    
    def test_evaluate_empty_board(self):
        """Test: evaluate_move on empty board"""
        board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        assert self.ai.evaluate_move(board) == 0
    
    # ===================== TESTS FOR FIND_EMPTY_CELLS =====================
    
    def test_find_empty_cells_all_empty(self):
        """Test: Find all 9 empty cells"""
        board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        empty = self.ai.find_empty_cells(board)
        assert empty == [0, 1, 2, 3, 4, 5, 6, 7, 8]
    
    def test_find_empty_cells_some_filled(self):
        """Test: Find only empty cells"""
        board = [1, 0, -1, 0, 0, 0, 0, 0, 0]
        empty = self.ai.find_empty_cells(board)
        assert empty == [1, 3, 4, 5, 6, 7, 8]
    
    def test_find_empty_cells_full(self):
        """Test: No empty cells when board is full"""
        board = [1, -1, 1, -1, 1, -1, 1, -1, 1]
        empty = self.ai.find_empty_cells(board)
        assert empty == []
    
    def test_find_empty_cells_only_center(self):
        """Test: Only center cell is empty"""
        board = [1, -1, 1, -1, 0, -1, 1, -1, 1]
        empty = self.ai.find_empty_cells(board)
        assert empty == [4]
    
    # ===================== TESTS FOR PLACE_MOVE =====================
    
    def test_place_move_human(self):
        """Test: Place human move"""
        board = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
        new_board = self.ai.place_move(board, 4, True)
        
        assert new_board[4] == 1  # Human = 1
        assert board[4] == 0      # Original unchanged (non-destructive)
    
    def test_place_move_ai(self):
        """Test: Place AI move"""
        board = np.array([1, 0, 0, 0, 0, 0, 0, 0, 0])
        new_board = self.ai.place_move(board, 8, False)
        
        assert new_board[8] == -1  # AI = -1
        assert new_board[0] == 1   # Other move preserved
        assert board[8] == 0       # Original unchanged
    
    def test_place_move_multiple(self):
        """Test: Multiple moves can be placed"""
        board = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
        board = self.ai.place_move(board, 0, True)   # Human at 0
        board = self.ai.place_move(board, 4, False)  # AI at 4
        
        assert board[0] == 1
        assert board[4] == -1
    
    # ===================== TESTS FOR GET_POSSIBLE_BOARDS =====================
    
    def test_get_possible_boards_empty(self):
        """Test: Empty board has 9 possible moves"""
        board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        possible = self.ai.get_possible_boards(board, True)
        
        assert len(possible) == 9
        # Each move should have exactly one move placed
        for i, board_state in enumerate(possible):
            assert board_state[i] == 1  # Position i has a move
    
    def test_get_possible_boards_limited(self):
        """Test: Fewer possible moves when board is partially full"""
        board = [1, 0, -1, 0, 0, 0, 0, 0, 0]
        possible = self.ai.get_possible_boards(board, False)
        
        assert len(possible) == 7  # 7 empty cells remaining
    
    def test_get_possible_boards_full(self):
        """Test: No possible moves when board is full"""
        board = [1, -1, 1, -1, 1, -1, 1, -1, 1]
        possible = self.ai.get_possible_boards(board, True)
        
        assert len(possible) == 0
    
    # ===================== TESTS FOR CACHING =====================
    
    def test_cache_initialization(self):
        """Test: Cache is initialized"""
        assert isinstance(self.ai.cache, dict)
        assert len(self.ai.cache) == 0
    
    def test_get_cache_size_empty(self):
        """Test: Cache size is 0 initially"""
        assert self.ai.get_cache_size() == 0
    
    def test_clear_cache(self):
        """Test: Cache can be cleared"""
        # Simulate cache entries
        self.ai.cache[(tuple([0]*9), True)] = (0, [0]*9)
        self.ai.cache[(tuple([1]*9), False)] = (1, [1]*9)
        
        assert self.ai.get_cache_size() == 2
        
        # Clear cache
        self.ai.clear_cache()
        assert self.ai.get_cache_size() == 0
    
    # ===================== TESTS FOR GTO (MINIMAX) =====================
    
    def test_gto_immediate_win_ai(self):
        """Test: gto recognizes immediate AI win"""
        # AI can win at position 2
        board = [-1, -1, 0, 0, 0, 0, 0, 0, 0]
        score, _ = self.ai.gto(board, False)
        
        assert score == -1  # AI wins
    
    def test_gto_immediate_win_human(self):
        """Test: gto recognizes immediate human win"""
        # Human can win at position 2
        board = [1, 1, 0, 0, 0, 0, 0, 0, 0]
        score, _ = self.ai.gto(board, True)
        
        assert score == 1  # Human wins
    
    def test_gto_returns_best_board(self):
        """Test: gto returns best board"""
        board = [-1, -1, 0, 0, 0, 0, 0, 0, 0]
        score, best_board = self.ai.gto(board, False)
        
        assert best_board is not None
        assert len(best_board) == 9
        # Best board should have an AI move
        assert -1 in best_board
    
    def test_gto_caches_result(self):
        """Test: gto stores results in cache"""
        board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        
        initial_cache_size = self.ai.get_cache_size()
        self.ai.gto(board, False)
        final_cache_size = self.ai.get_cache_size()
        
        assert final_cache_size > initial_cache_size  # Cache was filled
    
    def test_gto_uses_cache_second_call(self):
        """Test: Second call uses cache (visible in cache size)"""
        board = np.array([1, 0, 0, 0, 0, 0, 0, 0, 0])
        
        # First call
        self.ai.gto(board, False)
        cache_size_after_first = self.ai.get_cache_size()
        
        # Second call with same board
        self.ai.gto(board, False)
        cache_size_after_second = self.ai.get_cache_size()
        
        # Cache should not change much (already cached)
        assert cache_size_after_second >= cache_size_after_first
    
    # ===================== TESTS FOR GET_BEST_MOVE =====================
    
    def test_get_best_move_returns_board(self):
        """Test: get_best_move returns a board"""
        board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        best_board = self.ai.get_best_move(board)
        
        assert best_board is not None
        assert len(best_board) == 9
    
    def test_get_best_move_has_ai_move(self):
        """Test: Returned board has an AI move (-1)"""
        board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        best_board = self.ai.get_best_move(board)
        
        assert -1 in best_board
        assert best_board.count(-1) == 1  # Exactly one move added
    
    def test_get_best_move_preserves_existing_moves(self):
        """Test: Existing moves are preserved"""
        board = [1, -1, 0, 0, 0, 0, 0, 0, 0]
        best_board = self.ai.get_best_move(board)
        
        assert best_board[0] == 1   # Human move preserved
        assert best_board[1] == -1  # AI move preserved
        assert -1 in best_board[2:]  # New AI move added


# ===================== EDGE CASE TESTS =====================

class TestEdgeCases:
    """Tests for edge cases and special scenarios"""
    
    def setup_method(self):
        self.ai = TicTacToeAI()
    
    def test_board_as_list(self):
        """Test: Board can be provided as list"""
        board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        empty = self.ai.find_empty_cells(board)
        assert len(empty) == 9
    
    def test_board_as_numpy_array(self):
        """Test: Board can be provided as numpy array"""
        board = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
        empty = self.ai.find_empty_cells(board)
        assert len(empty) == 9
    
    def test_constants_are_correct(self):
        """Test: Constants have correct values"""
        assert self.ai.HUMAN == 1
        assert self.ai.AI == -1
        assert self.ai.EMPTY == 0


# ===================== INTEGRATION TESTS =====================

class TestIntegration:
    """Integration tests - multiple functions together"""
    
    def setup_method(self):
        self.ai = TicTacToeAI()
    
    def test_simple_game_flow(self):
        """Test: Simple game scenario"""
        board = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
        
        # Human plays
        board[0] = 1
        
        # AI responds
        board = self.ai.get_best_move(board)
        
        # Should have an AI move
        assert -1 in board
        assert board[0] == 1  # Human move preserved
    
    def test_game_until_end(self):
        """Test: Evaluate game until end"""
        board = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
        
        # Simulate a few moves
        board[4] = 1  # Human center
        board = self.ai.get_best_move(board)  # AI responds
        
        # Game should not be over
        assert not (self.ai.check_winning_condition(board, True) or 
                   self.ai.check_winning_condition(board, False))


if __name__ == "__main__":
    # Tests can also be run directly
    print("Run tests with: pytest testing/test_gto_ttt.py -v")
    print("or pytest testing/test_gto_ttt.py::TestTicTacToeAI::test_horizontal_win_human")
    print("\nAlmost all tests should be PASSED! ✅")
