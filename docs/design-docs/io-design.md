# I/O Module Design

## Overview
The `io` module provides terminal-based input/output functions for the chess game. It handles board rendering, move input parsing, and user interaction.

## Architecture

### Core Responsibilities
- **Board Rendering**: Display current board state to terminal
- **Input Parsing**: Parse user move input in various formats
- **User Interaction**: Display messages, game state, prompts
- **Move Validation**: Parse destination squares

### Key Components

#### I/O Module (`io.py`)
```
io.py
├── Board Display
│   └── render_board(board): ASCII art board rendering
├── Input Parsing
│   ├── parse_algebraic(move_str): Parse 'e2e4', 'Ke8', 'O-O'
│   └── parse_destination(move_str): Extract destination square
├── User Interaction
│   ├── get_user_input(prompt): Read user input with error handling
│   ├── display_message(msg): Show message to user
│   └── display_game_state(game): Show game status
└── Input Formats Supported
    ├── Simple: 'e2e4', 'e2 e4'
    ├── Piece notation: 'Ke8', 'Nf3'
    ├── Castling: 'O-O', 'O-O-O'
    └── Capture: 'exd5', 'Nxd5'
```

## Data Structures

### Algebraic Notation Formats
```
Simple move:     e2e4     (from, to)
With space:      e2 e4    (from space to)
Piece move:      Ke8      (King to e8)
Piece capture:   Nxf3     (Knight captures f3)
Castling:        O-O      (Kingside), O-O-O (Queenside)
Capture with:    exd5     (pawn from e-file captures d5)
```

## Algorithm Descriptions

### Board Rendering (`render_board`)
1. Print header with file labels (a-h)
2. Print top border
3. For each row (rank 8 to 1):
   - Print rank number and left border
   - Print each square (piece or empty)
   - Print right border
4. Print bottom border
5. Print file labels again

### Piece Symbols
```
White: ♔ ♕ ♖ ♗ ♘ ♙
Black: ♚ ♛ ♜ ♝ ♞ ♟
Empty: ·
```

### Move Parsing (`parse_algebraic`)
1. Handle castling: 'O-O' → ('', 'g1'/'g8'), 'O-O-O' → ('', 'c1'/'c8')
2. For standard moves (4 chars):
   - Extract from square: first 2 chars
   - Extract to square: last 2 chars
3. For piece notation (3-5 chars):
   - First char is piece symbol
   - Last 2 chars are destination
4. For capture notation:
   - Handle 'exd5' format (pawn from e-file captures d5)

### Destination Parsing (`parse_destination`)
1. Handle castling: return 'g1'/'c1' for white, 'g8'/'c8' for black
2. Find last digit in move string
3. Extract file and rank before the digit
4. Return destination square in algebraic notation

## Dependencies

### Imports
- `Board` from `chess.board`: Board object for rendering
- `Piece` from `chess.pieces`: Piece types for display
- `Game` from `chess.game`: Game object for state display

### No Circular Dependencies
- io.py depends on chess modules, but they don't depend on io.py
- Allows clean separation of concerns

## Error Handling

### parse_algebraic
- Raises `ValueError` for unrecognized formats
- Supports multiple formats for flexibility

### parse_destination
- Raises `ValueError` if destination cannot be determined
- Handles standard and castling moves

### get_user_input
- Returns empty string on EOF (Ctrl+D)
- Continues on empty input (re-prompts)

## Display Functions

### display_message(msg)
- Simple print wrapper for consistency

### display_game_state(game)
- Shows current player
- Checks for check/checkmate/stalemate
- Displays game result if applicable

## Usage Examples

```python
from chess.io import render_board, parse_algebraic, get_user_input

# Render board
render_board(game.board)

# Parse move input
move_str = get_user_input("Enter your move: ")
start, end = parse_algebraic(move_str)

# Display game state
display_game_state(game)
```

## Future Enhancements
- Colorized board output
- Move history display
- Move hints and annotations
- Input history navigation (arrow keys)
- Multi-line move notation support
- Game replay mode
- Export board to image/PDF
