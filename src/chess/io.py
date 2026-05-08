from typing import Tuple, Optional, List

from .board import Board
from .pieces import Piece
from .game import Game


def render_board(board: Board) -> None:
    """Render the chess board to the terminal.
    
    Args:
        board: Board instance to render
    """
    print("\n   a b c d e f g h")
    print("  ┌─────────────────┐")
    
    for row in range(8):
        rank = 8 - row
        row_str = f"{rank} │"
        for col in range(8):
            piece = board.get_piece(row, col)
            if piece is None:
                row_str += " ·"
            else:
                row_str += f" {piece.symbol}"
        row_str += " │"
        print(row_str)
    
    print("  └─────────────────┘")
    print("   a b c d e f g h\n")


def parse_algebraic(move_str: str) -> Tuple[str, str]:
    """Parse algebraic notation move string.
    
    Args:
        move_str: Move string like 'e2e4', 'Ke8', 'O-O'
        
    Returns:
        Tuple of (from_square, to_square)
        
    Raises:
        ValueError: If move format is invalid
    """
    move_str = move_str.strip()
    
    # Castling (white)
    if move_str == 'O-O':
        return ('e1', 'g1')
    if move_str == 'O-O-O':
        return ('e1', 'c1')
    
    # Castling (black)
    if move_str == 'O-O':
        return ('e8', 'g8')
    if move_str == 'O-O-O':
        return ('e8', 'c8')
    
    # Standard moves
    # Check for piece moves (uppercase letter at start like Ke8, Nf3, Bb5)
    if len(move_str) == 3 and move_str[0].isupper() and move_str[1].isalpha() and move_str[2].isdigit():
        # Piece move: Ke8, Nf3, Bb5
        return ('', move_str[1:3])
    elif len(move_str) == 4 and move_str[0].isupper() and move_str[1].isalpha():
        # Piece capture with file: Nbd5, Qxd5
        return ('', move_str[2:4])
    elif len(move_str) == 4:
        # Simple move: e2e4
        return (move_str[0:2], move_str[2:4])
    elif len(move_str) == 3 and move_str[1] == 'x':
        # Capture without from file: exd5
        return (move_str[0] + move_str[2], move_str[3:5])
    
    raise ValueError(f"Invalid move format: {move_str}")


def parse_destination(move_str: str) -> str:
    """Parse destination square from algebraic notation.
    
    Args:
        move_str: Move string like 'e2e4', 'Ke8', 'Nxe7'
        
    Returns:
        Destination square in algebraic notation
    """
    move_str = move_str.strip()
    
    # Castling (white)
    if move_str == 'O-O':
        return 'g1'
    if move_str == 'O-O-O':
        return 'c1'
    
    # Castling (black)
    if move_str == 'O-O':
        return 'g8'
    if move_str == 'O-O-O':
        return 'c8'
    
    # Extract destination
    for i in range(len(move_str) - 1, -1, -1):
        if move_str[i].isdigit():
            if i >= 1 and move_str[i-1].isalpha():
                return move_str[i-1:i+1]
    
    raise ValueError(f"Could not parse destination from: {move_str}")


def get_user_input(prompt: str = "Enter your move: ") -> str:
    """Get move input from user.
    
    Args:
        prompt: Input prompt string
        
    Returns:
        User input string
    """
    try:
        return input(prompt)
    except EOFError:
        return 'quit'


def display_message(message: str, type: str = 'info') -> None:
    """Display a message to the user.
    
    Args:
        message: Message text to display
        type: Message type ('info', 'error', 'success', 'warning')
    """
    prefixes = {
        'info': '',
        'error': 'ERROR: ',
        'success': '✓ ',
        'warning': '⚠ '
    }
    
    prefix = prefixes.get(type, '')
    print(f"{prefix}{message}")


def display_game_state(game: Game) -> None:
    """Display current game state.
    
    Args:
        game: Current Game instance
    """
    print(f"\n--- Move {game.move_number} ---")
    print(f"Current player: {game.current_player.capitalize()}")
    
    if game.get_game_state() == 'active':
        from chess.rules import is_in_check
        opponent = 'black' if game.current_player == 'white' else 'white'
        if is_in_check(game.board, opponent):
            print("Check!")
    else:
        winner = game.get_winner()
        if winner:
            print(f"Checkmate! {winner.capitalize()} wins!")
        else:
            print("Stalemate! Draw.")
