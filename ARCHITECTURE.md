# ARCHITECTURE.md

Written by team-lead before spawning teammates. This is the shared blueprint —
teammates read it to understand what they are building and how their module fits.
Update it when the structure changes; do not let it drift from the actual code.

## Module Structure

- `src/chess/board.py`: 8x8 board state with piece positioning, move history tracking
- `src/chess/pieces.py`: Piece classes (King, Queen, Rook, Bishop, Knight, Pawn) with move validation logic
- `src/chess/rules.py`: Check/checkmate detection, castling, en passant, pawn promotion rules
- `src/chess/game.py`: Game state management, turn handling, move execution, game loop
- `src/chess/io.py`: Terminal I/O (board rendering, move input parsing, output display)
- `src/chess/__init__.py`: Package exports and main entry point
- `main.py`: Entry point that initializes and runs the game

## Interfaces

### board.py
- `Board`: Class representing 8x8 chess board
  - `get_piece(row, col)` -> Piece | None
  - `set_piece(row, col, piece)` -> None
  - `copy()` -> Board: Deep copy for move validation
  - `is_valid_position(row, col)` -> bool

### pieces.py
- `Piece` (abstract base class)
  - `symbol` -> str: Unicode representation
  - `color` -> str: 'white' or 'black'
  - `get_valid_moves(board, from_row, from_col)` -> list[tuple[int, int]]: Relative moves without check validation
  - `can_reach(board, from_row, from_col, to_row, to_col)` -> bool

- `Pawn`, `Rook`, `Knight`, `Bishop`, `Queen`, `King` implement Piece interface

### rules.py
- `is_in_check(board, color)` -> bool
- `get_all_valid_moves(board, color)` -> dict[tuple[int, int], list[tuple[int, int]]]: From positions to valid destinations
- `is_checkmate(board, color)` -> bool
- `is_stalemate(board, color)` -> bool
- `is_valid_castling(board, from_row, from_col, to_row, to_col, color)` -> bool
- `is_valid_en_passant(board, from_row, from_col, to_row, to_col, color)` -> bool
- `get_promotion_choice()` -> str: Get promotion piece choice from user (q, r, b, n)

### game.py
- `Game`: Main game controller
  - `__init__()` -> Game
  - `current_player` -> str
  - `board` -> Board
  - `move_history` -> list[dict]: Full move record
  - `play_move(from_square, to_square)` -> bool: Execute move, returns success
  - `parse_move(square)` -> tuple[int, int]: Convert algebraic notation (e.g., 'e2') to (row, col)
  - `get_game_state()` -> str: 'active', 'checkmate', 'stalemate'
  - `get_winner()` -> str | None

### io.py
- `render_board(board)` -> None: Print board to terminal
- `parse_algebraic(move_str)` -> tuple[str, str]: Parse 'Ke8' into ('K', 'e8')
- `parse_destination(square_str)` -> tuple[int, int]: Convert 'e2' to (row, col)
- `get_user_input()` -> str: Read move from stdin
- `display_message(msg)` -> None: Print game messages

## Shared Data Structures

### Square coordinates
- Internal: `(row, col)` where row 0 = rank 8, row 7 = rank 1, col 0 = file a, col 7 = file h
- User-facing: Algebraic notation like 'e2', 'Ke8' (King to e8)

### Move record structure
```python
{
    'move_number': int,
    'player': 'white' | 'black',
    'piece': str,  # 'K', 'Q', 'R', 'B', 'N', 'P'
    'from_square': tuple[int, int],
    'to_square': tuple[int, int],
    'captured': Piece | None,
    'is_castling': bool,
    'is_en_passant': bool,
    'is_promotion': bool,
    'promotion_piece': str | None,
    'is_check': bool,
    'is_checkmate': bool,
    'notation': str  # Full chess notation like 'O-O' or 'exd6'
}
```

### Game state
- Active game with white to move
- Check state
- Castling rights (white kingside, white queenside, black kingside, black queenside)
- En passant target square

## External Dependencies

- No external dependencies required
- Uses Python standard library only (sys, typing)
