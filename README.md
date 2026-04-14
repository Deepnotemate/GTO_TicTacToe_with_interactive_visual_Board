# Tic Tac Toe - Game Theory Optimal AI

A Python implementation of Tic Tac Toe with an AI opponent using Game Theory Optimization (GTO minimax algorithm).

## Overview

This project implements an unbeatable Tic Tac Toe AI using game-theoretic principles to find optimal moves. The AI analyzes all possible game states and selects moves that maximize its chances of winning or force a draw.

## Features

- **GTO Algorithm**: Minimax-based optimal play
- **Interactive Board**: Visual representation of the game board
- **Unbeatable AI**: AI plays optimally every move

## Project Structure

```
├── GTO_TTT.py              # Core game theory optimization engine
├── Interactive_Board.py    # Board visualization and rendering
├── testing/
│   └── tester.py          # Test cases
└── README.md
```

## Files

- **GTO_TTT.py**: Contains the minimax algorithm with:
  - `winning_condition()`: Check for winning states
  - `evaluate_move()`: Evaluate board positions
  - `gto()`: Main game-theoretic optimal decision engine

- **Interactive_Board.py**: Visualization functions:
  - `draw_board()`: Renders the 3x3 grid
  - `draw_circle()`: Draws player and AI moves

## Requirements

- Python 3.x
- numpy
- matplotlib

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from GTO_TTT import gto
from Interactive_Board import draw_board, draw_circle
```

## Future Improvements

- Implement player choice for who goes first
- Add randomization to GTO for varied gameplay
- Optimize code readability and performance
- Integrate machine learning components
- Add command-line interface

## License

MIT License

## Author

Created as a game theory learning project.
