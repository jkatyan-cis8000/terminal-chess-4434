"""Game controller for terminal chess."""

from typing import Dict, List, Tuple, Optional
from .board import Board
from .pieces import Piece, King, Pawn, Queen, Rook, Bishop, Knight
from .rules import (
    is_in_check, get_all_valid_moves, is_checkmate, is_stalemate,
    is_valid_castling, is_valid_en_passant, get_promotion_choice,
    get_promotion_piece, get_castling_rights
)


class Game:
    """Main game controller for chess."""
    
    def __init__(self) -> None:
        """Initialize a new chess game."""
        self.board = Board()
        self.current_player = 'white'
        self.move_history: List[Dict] = []
        self.move_number = 1
        self.castling_rights = {
            'white': {'kingside': True, 'queenside': True},
            'black': {'kingside': True, 'queenside': True}
        }
        self.en_passant_target: Optional[Tuple[int, int]] = None
        self._setup_board()
    
    def _setup_board(self) -> None:
        """Set up initial board position."""
        from .pieces import (
            Pawn, Rook, Knight, Bishop, Queen, King
        )
        
        # Place pawns
        for col in range(8):
            self.board.set_piece(6, col, Pawn('white'))
            self.board.set_piece(1, col, Pawn('black'))
        
        # Place major pieces
        back_row_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        
        for col, piece_class in enumerate(back_row_order):
            self.board.set_piece(7, col, piece_class('white'))
            self.board.set_piece(0, col, piece_class('black'))
    
    def parse_square(self, square: str) -> Tuple[int, int]:
        """Convert algebraic notation (e.g., 'e2') to (row, col)."""
        if len(square) != 2:
            raise ValueError(f"Invalid square: {square}")
        
        file = square[0].lower()
        rank = square[1]
        
        if file not in 'abcdefgh' or rank not in '12345678':
            raise ValueError(f"Invalid square: {square}")
        
        col = ord(file) - ord('a')
        row = 8 - int(rank)
        
        return (row, col)
    
    def to_algebraic(self, row: int, col: int) -> str:
        """Convert (row, col) to algebraic notation."""
        file = chr(ord('a') + col)
        rank = str(8 - row)
        return f"{file}{rank}"
    
    def play_move(self, from_square: str, to_square: str) -> bool:
        """Execute a move from from_square to to_square."""
        from_row, from_col = self.parse_square(from_square)
        to_row, to_col = self.parse_square(to_square)
        
        piece = self.board.get_piece(from_row, from_col)
        
        if not piece:
            return False
        
        if piece.color != self.current_player:
            return False
        
        # Check if move is valid
        valid_moves = piece.get_valid_moves(self.board, from_row, from_col)
        if (to_row, to_col) not in valid_moves:
            # Check for castling
            if isinstance(piece, King):
                temp_board = self.board.copy()
                temp_board.set_piece(from_row, from_col, None)
                temp_board.set_piece(to_row, to_col, piece)
                
                if is_valid_castling(self.board, from_row, from_col, to_row, to_col, self.current_player):
                    return self._execute_castle(from_row, from_col, to_row, to_col)
            
            return False
        
        # Check for en passant
        captured_piece = None
        is_en_passant = False
        if isinstance(piece, Pawn):
            if self.en_passant_target == (to_row, to_col):
                is_en_passant = True
                capture_row = from_row
                captured_piece = self.board.get_piece(capture_row, to_col)
        
        # Execute the move
        self.board.set_piece(to_row, to_col, piece)
        self.board.set_piece(from_row, from_col, None)
        piece.has_moved = True
        
        # Handle castling rook movement
        if isinstance(piece, King) and abs(to_col - from_col) == 2:
            if to_col == 6:  # Kingside
                rook = self.board.get_piece(from_row, 7)
                self.board.set_piece(from_row, 5, rook)
                self.board.set_piece(from_row, 7, None)
                rook.has_moved = True
            elif to_col == 2:  # Queenside
                rook = self.board.get_piece(from_row, 0)
                self.board.set_piece(from_row, 3, rook)
                self.board.set_piece(from_row, 0, None)
                rook.has_moved = True
        
        # Handle en passant capture
        if is_en_passant:
            capture_row = from_row
            self.board.set_piece(capture_row, to_col, None)
        
        # Update castling rights
        if isinstance(piece, King):
            self.castling_rights[self.current_player] = {'kingside': False, 'queenside': False}
        elif isinstance(piece, Rook):
            if from_col == 0:
                self.castling_rights[self.current_player]['queenside'] = False
            elif from_col == 7:
                self.castling_rights[self.current_player]['kingside'] = False
        
        # Set en passant target for next move
        self.en_passant_target = None
        if isinstance(piece, Pawn) and abs(to_row - from_row) == 2:
            self.en_passant_target = (from_row + (to_row - from_row) // 2, from_col)
        
        # Handle pawn promotion
        is_promotion = isinstance(piece, Pawn) and (to_row == 0 or to_row == 7)
        if is_promotion:
            promotion_choice = get_promotion_choice()
            self.board.set_piece(to_row, to_col, get_promotion_piece(promotion_choice, self.current_player))
        
        # Record the move
        self._record_move(from_row, from_col, to_row, to_col, piece, captured_piece, 
                         is_castling=isinstance(piece, King) and abs(to_col - from_col) == 2,
                         is_en_passant=is_en_passant,
                         is_promotion=is_promotion)
        
        # Switch player
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        self.move_number += 1
        
        return True
    
    def _execute_castle(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Execute a castling move."""
        piece = self.board.get_piece(from_row, from_col)
        
        # Move king
        self.board.set_piece(to_row, to_col, piece)
        self.board.set_piece(from_row, from_col, None)
        piece.has_moved = True
        
        # Move rook
        if to_col == 6:  # Kingside
            rook = self.board.get_piece(from_row, 7)
            self.board.set_piece(from_row, 5, rook)
            self.board.set_piece(from_row, 7, None)
            rook.has_moved = True
        elif to_col == 2:  # Queenside
            rook = self.board.get_piece(from_row, 0)
            self.board.set_piece(from_row, 3, rook)
            self.board.set_piece(from_row, 0, None)
            rook.has_moved = True
        
        # Update castling rights
        self.castling_rights[self.current_player] = {'kingside': False, 'queenside': False}
        
        # Record the move
        notation = 'O-O' if to_col == 6 else 'O-O-O'
        self._record_move(from_row, from_col, to_row, to_col, piece, None, 
                         is_castling=True, is_en_passant=False, is_promotion=False)
        
        # Switch player
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        
        return True
    
    def _record_move(self, from_row: int, from_col: int, to_row: int, to_col: int,
                    piece: Piece, captured: Optional[Piece], 
                    is_castling: bool, is_en_passant: bool, is_promotion: bool) -> None:
        """Record a move in the history."""
        piece_symbol = type(piece).__name__[0] if not isinstance(piece, Pawn) else ''
        notation = f"{piece_symbol}{self.to_algebraic(to_row, to_col)}"
        
        if is_castling:
            notation = 'O-O' if to_col == 6 else 'O-O-O'
        elif is_en_passant:
            notation = f"{self.to_algebraic(from_row, from_col)[0]}x{self.to_algebraic(to_row, to_col)} e.p."
        
        if is_promotion:
            notation += "=Q"  # Simplified: always show Q for now
        
        self.move_history.append({
            'move_number': self.move_number,
            'player': self.current_player,
            'piece': piece_symbol,
            'from_square': (from_row, from_col),
            'to_square': (to_row, to_col),
            'captured': captured,
            'is_castling': is_castling,
            'is_en_passant': is_en_passant,
            'is_promotion': is_promotion,
            'notation': notation
        })
    
    def get_game_state(self) -> str:
        """Get current game state: 'active', 'checkmate', or 'stalemate'."""
        if is_checkmate(self.board, self.current_player):
            return 'checkmate'
        if is_stalemate(self.board, self.current_player):
            return 'stalemate'
        return 'active'
    
    def get_winner(self) -> Optional[str]:
        """Get winner if game is over."""
        if self.get_game_state() == 'checkmate':
            return 'black' if self.current_player == 'white' else 'white'
        return None
    
    def is_in_check(self) -> bool:
        """Check if current player's king is in check."""
        return is_in_check(self.board, self.current_player)
    
    def get_all_valid_moves(self) -> Dict[Tuple[int, int], List[Tuple[int, int]]]:
        """Get all valid moves for current player."""
        return get_all_valid_moves(self.board, self.current_player)
