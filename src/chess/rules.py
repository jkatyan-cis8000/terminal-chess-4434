"""Chess rules engine: check, checkmate, castling, en passant, promotion."""

from typing import Dict, List, Tuple, Optional
from .board import Board
from .pieces import Piece, King, Pawn


def is_in_check(board: Board, color: str) -> bool:
    """Check if the king of given color is under attack."""
    # Find king position
    king_pos = None
    for row in range(8):
        for col in range(8):
            piece = board.get_piece(row, col)
            if isinstance(piece, King) and piece.color == color:
                king_pos = (row, col)
                break
        if king_pos:
            break
    
    if not king_pos:
        return False
    
    # Check if any opponent piece can attack the king
    opponent_color = 'black' if color == 'white' else 'white'
    for row in range(8):
        for col in range(8):
            piece = board.get_piece(row, col)
            if piece and piece.color == opponent_color:
                moves = piece.get_valid_moves(board, row, col)
                if king_pos in moves:
                    return True
    
    return False


def get_all_valid_moves(board: Board, color: str) -> Dict[Tuple[int, int], List[Tuple[int, int]]]:
    """Get all legal moves for a color (excluding moves that leave king in check)."""
    valid_moves = {}
    
    for row in range(8):
        for col in range(8):
            piece = board.get_piece(row, col)
            if piece and piece.color == color:
                moves = piece.get_valid_moves(board, row, col)
                legal_moves = []
                
                for to_row, to_col in moves:
                    # Simulate move and check if king is left in check
                    temp_board = board.copy()
                    temp_board.set_piece(to_row, to_col, temp_board.get_piece(row, col))
                    temp_board.set_piece(row, col, None)
                    
                    if not is_in_check(temp_board, color):
                        legal_moves.append((to_row, to_col))
                
                if legal_moves:
                    valid_moves[(row, col)] = legal_moves
    
    return valid_moves


def is_checkmate(board: Board, color: str) -> bool:
    """Check if the given color is in checkmate."""
    if not is_in_check(board, color):
        return False
    
    # Check if any legal move exists
    valid_moves = get_all_valid_moves(board, color)
    return len(valid_moves) == 0


def is_stalemate(board: Board, color: str) -> bool:
    """Check if the given color is in stalemate."""
    if is_in_check(board, color):
        return False
    
    # Check if any legal move exists
    valid_moves = get_all_valid_moves(board, color)
    return len(valid_moves) == 0


def get_castling_rights(board: Board, color: str) -> Dict[str, bool]:
    """Get castling rights for the given color."""
    rights = {
        'kingside': False,
        'queenside': False
    }
    
    # Find king and rooks
    king_row = 7 if color == 'white' else 0
    
    # Check if king has moved
    king = board.get_piece(king_row, 4)
    if not isinstance(king, King) or king.has_moved:
        return rights
    
    # Check kingside rook
    rook = board.get_piece(king_row, 7)
    if isinstance(rook, Piece) and rook.color == color and not rook.has_moved:
        # Check path is clear
        if board.get_piece(king_row, 5) is None and board.get_piece(king_row, 6) is None:
            # Check not in check or passing through check
            if not is_in_check(board, color):
                temp_board = board.copy()
                temp_board.set_piece(king_row, 5, temp_board.get_piece(king_row, 4))
                temp_board.set_piece(king_row, 4, None)
                if not is_in_check(temp_board, color):
                    rights['kingside'] = True
    
    # Check queenside rook
    rook = board.get_piece(king_row, 0)
    if isinstance(rook, Piece) and rook.color == color and not rook.has_moved:
        # Check path is clear
        if (board.get_piece(king_row, 1) is None and 
            board.get_piece(king_row, 2) is None and 
            board.get_piece(king_row, 3) is None):
            # Check not in check or passing through check
            if not is_in_check(board, color):
                temp_board = board.copy()
                temp_board.set_piece(king_row, 3, temp_board.get_piece(king_row, 4))
                temp_board.set_piece(king_row, 4, None)
                if not is_in_check(temp_board, color):
                    rights['queenside'] = True
    
    return rights


def is_valid_castling(board: Board, from_row: int, from_col: int, 
                      to_row: int, to_col: int, color: str) -> bool:
    """Check if castling move is valid."""
    if from_row != to_row:
        return False
    
    king_row = 7 if color == 'white' else 0
    if from_row != king_row or from_col != 4 or to_col not in [2, 6]:
        return False
    
    rights = get_castling_rights(board, color)
    if to_col == 6 and rights['kingside']:
        return True
    if to_col == 2 and rights['queenside']:
        return True
    
    return False


def is_valid_en_passant(board: Board, from_row: int, from_col: int,
                        to_row: int, to_col: int, color: str) -> bool:
    """Check if en passant capture is valid."""
    piece = board.get_piece(from_row, from_col)
    if not isinstance(piece, Pawn) or piece.color != color:
        return False
    
    # En passant only works for pawns moving diagonally forward
    direction = -1 if color == 'white' else 1
    if to_row != from_row + direction:
        return False
    
    # Check if destination square is empty (en passant capture)
    if board.get_piece(to_row, to_col) is not None:
        return False
    
    # Check if there's an enemy pawn at the capture position
    capture_row = from_row
    capture_col = to_col
    captured_piece = board.get_piece(capture_row, capture_col)
    
    if not captured_piece or not isinstance(captured_piece, Pawn):
        return False
    
    if captured_piece.color == color:
        return False
    
    return True


def get_promotion_choice() -> str:
    """Get promotion piece choice from user (q, r, b, n)."""
    while True:
        choice = input("Choose promotion (q=Queen, r=Rook, b=Bishop, n=Knight): ").lower()
        if choice in ['q', 'r', 'b', 'n']:
            return choice
        print("Invalid choice. Please enter q, r, b, or n.")


def get_promotion_piece(symbol: str, color: str) -> Piece:
    """Create promotion piece from symbol."""
    from .pieces import Queen, Rook, Bishop, Knight
    
    pieces = {'q': Queen, 'r': Rook, 'b': Bishop, 'n': Knight}
    return pieces[symbol](color)
