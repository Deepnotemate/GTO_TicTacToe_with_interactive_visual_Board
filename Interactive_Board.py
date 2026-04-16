import time

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb

from GTO_TTT import TicTacToeAI

BOARD_SIZE = 3
DEFAULT_CELL_SIZE = 100
GRID_COLOR = 'gray'
MARK_COLOR_CROSS = 30
MARK_COLOR_CIRCLE = 30
HIGHLIGHT_COLOR = 60
AI_DELAY_SECONDS = 0.35
RESULT_DELAY_SECONDS = 2
CLOSE_DELAY_SECONDS = 1


class TicTacToeGame:
    """Interactive matplotlib board for playing Tic-Tac-Toe against the AI."""

    def __init__(self, human_goes_first: bool | None = None, cell_size: int = DEFAULT_CELL_SIZE):
        self.N = cell_size
        self.agent = TicTacToeAI()
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect('equal')
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.human_goes_first = human_goes_first

        self.boards: list[np.ndarray] = []
        self.selections = self._create_selections()
        self.current_selection = self.selections[0]
        self.cross = False
        self.placeholder = False
        self.marker = None
        self._grid_drawn = False

    def _create_selections(self) -> np.ndarray:
        """Create one-hot encoded board selections for all 9 cells."""
        selections = np.zeros((9, BOARD_SIZE, BOARD_SIZE))
        for index in range(9):
            selections[index].ravel()[index] = 1
        return selections

    def _prompt_first_player(self) -> bool:
        """Ask who should start only when the interactive game is launched."""
        if self.human_goes_first is None:
            answer = input('Do you want to go first? (y/any key): ').strip().lower()
            self.human_goes_first = answer == 'y'
        return self.human_goes_first

    def _current_board_state(self) -> np.ndarray:
        """Return the current aggregated board state."""
        if not self.boards:
            return np.zeros((BOARD_SIZE, BOARD_SIZE))
        return np.sum(self.boards, axis=0)

    def _board_is_full(self, board: np.ndarray) -> bool:
        """Return True if there are no empty cells left."""
        return self.agent.is_board_full(board.ravel())

    def _cycle_selection(self, step: int) -> None:
        """Move the selection cursor horizontally."""
        current_index = int(np.argmax(self.current_selection.ravel()))
        row, col = divmod(current_index, BOARD_SIZE)
        new_col = (col + step) % BOARD_SIZE
        self.current_selection = self.selections[row * BOARD_SIZE + new_col]

    def _move_selection_vertical(self, step: int) -> None:
        """Move the selection cursor vertically on the 3x3 board."""
        current_index = int(np.argmax(self.current_selection.ravel()))
        row, col = divmod(current_index, BOARD_SIZE)
        new_row = (row + step) % BOARD_SIZE
        self.current_selection = self.selections[new_row * BOARD_SIZE + col]

    def _apply_move(self, move_index: int) -> None:
        """Add the current move to the board history."""
        selection = self.selections[move_index]
        self.boards.append(selection if self.cross else selection * -1)

    def _refresh_marker(self) -> None:
        """Redraw the board and current selection highlight."""
        board = self.visualize_game_state(self._current_board_state())
        board = self.highlight_move(board, self.current_selection, self.cross)
        if self.marker is not None:
            self.marker.set_data(board)
            self.fig.canvas.draw_idle()

    def _announce_result(self, winner: bool | None) -> None:
        """Show the game result and close the board."""
        if winner is None:
            print('This is a Tie!')
        elif not winner:
            print('Human wins the game!')
        else:
            print('AI wins the game!')
        time.sleep(RESULT_DELAY_SECONDS)
        print('Thank You for playing!')
        time.sleep(CLOSE_DELAY_SECONDS)
        plt.close('all')

    def _choose_ai_move(self, flat_board: np.ndarray) -> int:
        """Select the AI move using the existing heuristics and GTO engine."""
        new_board = self.agent.gto(flat_board, self.cross)[1]
        return int(np.argmax(np.abs(new_board - flat_board)))

    def draw_board(self) -> np.ndarray:
        """Create the board canvas and draw the grid once."""
        if not self._grid_drawn:
            for position in range(1, BOARD_SIZE):
                self.ax.axvline(position * self.N, color=GRID_COLOR)
                self.ax.axhline(position * self.N, color=GRID_COLOR)
            self._grid_drawn = True
        return np.zeros((BOARD_SIZE * self.N, BOARD_SIZE * self.N))

    def draw_circle(self, board: np.ndarray, move: np.ndarray, color: float = MARK_COLOR_CIRCLE) -> np.ndarray:
        """Draw a circle marker on the selected cell."""
        rows, cols = np.ogrid[:self.N, :self.N]
        center = (self.N - 1) / 2
        distance = (rows - center) ** 2 + (cols - center) ** 2
        circle_mask = ((self.N / 5) ** 2 <= distance) & (distance <= (self.N / 4) ** 2)
        circle = circle_mask.astype(float) * color
        board += np.kron(move.reshape(BOARD_SIZE, BOARD_SIZE), circle)
        return board

    def draw_cross(self, board: np.ndarray, move: np.ndarray, color: float = MARK_COLOR_CROSS) -> np.ndarray:
        """Draw a cross marker on the selected cell."""
        rows, cols = np.indices((self.N, self.N))
        padding_mask = (rows > 10) & (rows < self.N - 10) & (cols > 10) & (cols < self.N - 10)
        cross_mask = (np.abs(rows - cols) <= 1) | (np.abs(rows + cols - (self.N - 1)) <= 1)
        cross = (cross_mask & padding_mask).astype(float) * color
        board += np.kron(move.reshape(BOARD_SIZE, BOARD_SIZE), cross)
        return board

    def visualize_game_state(self, board: np.ndarray) -> np.ndarray:
        """Convert a 3x3 game state into a rendered board image."""
        rendered_board = self.draw_board()
        base_move = np.zeros(9)
        for index, value in enumerate(board.ravel()):
            if value == 0:
                continue
            move = base_move.copy()
            move[index] = 1
            if value == 1:
                rendered_board = self.draw_cross(rendered_board, move)
            else:
                rendered_board = self.draw_circle(rendered_board, move)
        return rendered_board

    def highlight_move(self, board: np.ndarray, move: np.ndarray, cross: bool = False) -> np.ndarray:
        """Overlay the currently selected move with a highlight."""
        if cross:
            board = self.draw_cross(board, move, MARK_COLOR_CROSS)
        else:
            board = self.draw_circle(board, move, MARK_COLOR_CIRCLE)
        board += np.kron(move.reshape(BOARD_SIZE, BOARD_SIZE), HIGHLIGHT_COLOR * np.ones((self.N, self.N)))
        return board

    def check_winner(self, board: np.ndarray) -> tuple[bool, bool | None]:
        """Check whether the board has a winner using the shared AI logic."""
        winner = self.agent.get_winner(board.ravel())
        return winner is not None, winner

    def on_key(self, event) -> None:
        """Handle keyboard interaction for moving and placing selections."""
        current_board = self._current_board_state()

        if self.placeholder:
            _, winner = self.check_winner(current_board)
            self._announce_result(winner)
            return

        if self._board_is_full(current_board):
            self._announce_result(None)
            return

        if event.key == 'right':
            self._cycle_selection(1)
            self._refresh_marker()
            return

        if event.key == 'left':
            self._cycle_selection(-1)
            self._refresh_marker()
            return

        if event.key == 'up':
            self._move_selection_vertical(-1)
            self._refresh_marker()
            return

        if event.key == 'down':
            self._move_selection_vertical(1)
            self._refresh_marker()
            return

        if event.key != 'enter':
            return

        move_index = int(np.argmax(self.current_selection.ravel()))
        if current_board.ravel()[move_index] != 0:
            print('That space is already taken!')
            return

        self._apply_move(move_index)
        self._refresh_marker()

        current_board = self._current_board_state()
        win, winner = self.check_winner(current_board)
        if win:
            self.placeholder = True
            self._announce_result(winner)
            return

        if self._board_is_full(current_board):
            self._announce_result(None)
            return

        self.cross = not self.cross
        time.sleep(AI_DELAY_SECONDS)

        ai_move_index = self._choose_ai_move(current_board.ravel())
        self.current_selection = self.selections[ai_move_index]
        self._apply_move(ai_move_index)
        self._refresh_marker()
        self.cross = not self.cross

        win, winner = self.check_winner(self._current_board_state())
        if win:
            self.placeholder = True

    def initialize_game(self) -> None:
        """Initialize the game state and render the starting board."""
        self.draw_board()
        self.boards = []

        if not self._prompt_first_player():
            first_move = np.zeros(9)
            first_move[np.random.randint(9)] = 1
            self.boards.append(first_move.reshape(BOARD_SIZE, BOARD_SIZE))

        board = self.visualize_game_state(self._current_board_state())
        highlighted = self.highlight_move(board, self.current_selection, cross=self.cross)
        self.marker = self.ax.imshow(highlighted, cmap='gist_earth')
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)

    def run(self) -> None:
        """Start the interactive game window."""
        self.initialize_game()
        plt.show()


