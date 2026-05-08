# Game Controller Design

## Overview
The `Game` class is the main controller for the chess game, managing game state, move execution, and rule validation. It coordinates between the board, pieces, and rules modules.

## Architecture

### Core Responsibilities
- **State Management**: Track current player, move history, game phase (active/checkmate/stalemate)
- **Move Execution**: Validate and execute moves, update board state
- **Rule Coordination**: Delegate rule checking to the rules module
- **Move Notation**: Generate and record move notation in history

### Key Components

#### Game Class (`game.py`)
```
Game
├── State
│   ├── current_player: str
│   ├── board: Board
│   ├── move_history: List[MoveRecord]
│   ├── move_number: int
│   ├── castling_rights: Dict[str, Dict[str, bool]]
│   └── en_passant_target: Optional[Tuple[int, int]]
├── Initialization
│   └── __init__(): Setup board, set white as first player
├── Move Execution
│   ├── play_move(from_square, to_square): Execute validated move
│   ├── parse_move(move_str): Parse algebraic notation
│   └── get_game_state(): Check for checkmate/stalemate
└── Utility
    ├── get_winner(): Return winner if game over
    ├── is_valid_move(): Validate move against current state
    └── undo_move(): Revert last move (future enhancement)
```

## Data Structures

### MoveRecord
```python
MoveRecord = {
    'move_number': int,
    'player': 'white' | 'black',
    'piece': str,  # Piece symbol (K, Q, R, B, N, P)
    'from_square': Tuple[int, int],  # (row, col)
    'to_square': Tuple[int, int],
    'captured': Optional[Piece],
    'is_castling': bool,
    'is_en_passant': bool,
    'is_promotion': bool,
    'promotion_piece': Optional[str],  # Q, R, B, N if promotion
    'notation': str  # Algebraic notation (e.g., 'Nf3', 'O-O')
}
```

## Algorithm Descriptions

### Move Execution Flow (`play_move`)
1. Parse source and destination squares from input
2. Get piece at source square
3. Validate move using rules module
4. Handle special cases:
   - **Castling**: Move both king and rook
   - **En Passant**: Remove captured pawn
   - **Promotion**: Replace pawn with queen (auto-promotion)
5. Record move in history
6. Switch current player
7. Update castling rights if king/rook moved
8. Set en passant target if pawn moved 2 squares

### Move Notation Generation
- **Standard moves**: e.g., 'Nf3' (knight to f3)
- **Captures**: e.g., 'exd5' (pawn from e-file captures on d5)
- **Castling**: 'O-O' (kingside), 'O-O-O' (queenside)
- **Check**: '+' suffix
- **Checkmate**: '#' suffix

## Dependencies

### Imports
- `Board` from `chess.board`: Board state and piece positioning
- `Piece` and subclasses from `chess.pieces`: Piece types and movement rules
- Rule functions from `chess.rules`: Validation and game state detection

### Integration Points
- **Board**: Game uses Board for piece positioning and manipulation
- **Pieces**: Game creates pieces for initial setup and handles promotion
- **Rules**: Game delegates move validation and game state checks

## Error Handling
- Invalid square format: `ValueError`
- No piece at source: `ValueError`
- Invalid move: `ValueError`
- Move during game over: `ValueError`

## Future Enhancements
- Undo/redo functionality
- Move validation hints
- Multiple promotion choice (Q, R, B, N)
- Game save/load
- Player vs AI
- Multiplayer network support
