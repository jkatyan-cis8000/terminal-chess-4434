from abc import ABC, abstractmethod
from typing import Tuple, List, Optional

from .board import Board


class Piece(ABC):
    """Abstract base class for chess pieces."""
    
    def __init__(self, symbol: str, color: str) -> None:
        """
        Initialize piece.
        
        Args:
            symbol: Unicode representation of the piece
            color: 'white' or 'black'
        """
        self.symbol = symbol
        self.color = color
        self.has_moved = False
    
    @abstractmethod
    def get_valid_moves(self, board: Board, from_row: int, from_col: int) -> List[Tuple[int, int]]:
        """
        Get all valid moves from position without check validation.
        
        Args:
            board: Current board state
            from_row: Source row (0 = rank 8)
            from_col: Source column (0 = file a)
        
        Returns:
            List of (row, col) positions the piece can move to
        """
        pass
    
    @abstractmethod
    def can_reach(self, board: Board, from_row: int, from_col: int, 
                  to_row: int, to_col: int) -> bool:
        """
        Check if piece can reach target position.
        
        Args:
            board: Current board state
            from_row: Source row
            from_col: Source column
            to_row: Target row
            to_col: Target column
        
        Returns:
            True if piece can move to target position
        """
        pass


class Pawn(Piece):
    """Pawn piece with special first move and capture logic."""
    
    def __init__(self, color: str) -> None:
        super().__init__('♙' if color == 'white' else '♟', color)
    
    def get_valid_moves(self, board: Board, from_row: int, from_col: int) -> List[Tuple[int, int]]:
        """Get valid pawn moves including single step, double step on first move, and captures."""
        moves = []
        direction = -1 if self.color == 'white' else 1
        start_row = 6 if self.color == 'white' else 1
        
        # Single step forward
        new_row = from_row + direction
        if board.is_valid_position(new_row, from_col) and board.get_piece(new_row, from_col) is None:
            moves.append((new_row, from_col))
            
            # Double step on first move
            if from_row == start_row:
                new_row_double = from_row + 2 * direction
                if board.is_valid_position(new_row_double, from_col) and board.get_piece(new_row_double, from_col) is None:
                    moves.append((new_row_double, from_col))
        
        # Capture diagonally
        for col_offset in [-1, 1]:
            new_row = from_row + direction
            new_col = from_col + col_offset
            if board.is_valid_position(new_row, new_col):
                target_piece = board.get_piece(new_row, new_col)
                if target_piece is not None and target_piece.color != self.color:
                    moves.append((new_row, new_col))
        
        return moves
    
    def can_reach(self, board: Board, from_row: int, from_col: int, 
                  to_row: int, to_col: int) -> bool:
        """Check if pawn can reach target position."""
        direction = -1 if self.color == 'white' else 1
        start_row = 6 if self.color == 'white' else 1
        
        # Forward move (single or double)
        if to_col == from_col:
            if to_row == from_row + direction:
                return board.get_piece(to_row, to_col) is None
            if from_row == start_row and to_row == from_row + 2 * direction:
                return (board.get_piece(from_row + direction, from_col) is None and 
                        board.get_piece(to_row, to_col) is None)
        
        # Diagonal capture
        if abs(to_col - from_col) == 1 and to_row == from_row + direction:
            target_piece = board.get_piece(to_row, to_col)
            return target_piece is not None and target_piece.color != self.color
        
        return False


class Rook(Piece):
    """Rook piece - moves horizontally and vertically."""
    
    def __init__(self, color: str) -> None:
        super().__init__('♖' if color == 'white' else '♜', color)
    
    def get_valid_moves(self, board: Board, from_row: int, from_col: int) -> List[Tuple[int, int]]:
        """Get valid rook moves (horizontal and vertical lines)."""
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for dr, dc in directions:
            row, col = from_row + dr, from_col + dc
            while board.is_valid_position(row, col):
                target = board.get_piece(row, col)
                if target is None:
                    moves.append((row, col))
                elif target.color != self.color:
                    moves.append((row, col))
                    break
                else:
                    break
                row += dr
                col += dc
        
        return moves
    
    def can_reach(self, board: Board, from_row: int, from_col: int, 
                  to_row: int, to_col: int) -> bool:
        """Check if rook can reach target position."""
        if from_row != to_row and from_col != to_col:
            return False
        
        if from_row == to_row:
            step = 1 if to_col > from_col else -1
            for col in range(from_col + step, to_col, step):
                if board.get_piece(from_row, col) is not None:
                    return False
            return True
        
        if from_col == to_col:
            step = 1 if to_row > from_row else -1
            for row in range(from_row + step, to_row, step):
                if board.get_piece(row, from_col) is not None:
                    return False
            return True
        
        return False


class Knight(Piece):
    """Knight piece - moves in L-shape."""
    
    def __init__(self, color: str) -> None:
        super().__init__('♘' if color == 'white' else '♞', color)
    
    def get_valid_moves(self, board: Board, from_row: int, from_col: int) -> List[Tuple[int, int]]:
        """Get valid knight moves (L-shape: 2 in one direction, 1 in perpendicular)."""
        moves = []
        offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), 
                   (1, -2), (1, 2), (2, -1), (2, 1)]
        
        for dr, dc in offsets:
            row, col = from_row + dr, from_col + dc
            if board.is_valid_position(row, col):
                target = board.get_piece(row, col)
                if target is None or target.color != self.color:
                    moves.append((row, col))
        
        return moves
    
    def can_reach(self, board: Board, from_row: int, from_col: int, 
                  to_row: int, to_col: int) -> bool:
        """Check if knight can reach target position."""
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)
        
        is_l_shape = (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)
        if not is_l_shape:
            return False
        
        target = board.get_piece(to_row, to_col)
        if target is None:
            return True
        return target.color != self.color


class Bishop(Piece):
    """Bishop piece - moves diagonally."""
    
    def __init__(self, color: str) -> None:
        super().__init__('♗' if color == 'white' else '♝', color)
    
    def get_valid_moves(self, board: Board, from_row: int, from_col: int) -> List[Tuple[int, int]]:
        """Get valid bishop moves (diagonals)."""
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dr, dc in directions:
            row, col = from_row + dr, from_col + dc
            while board.is_valid_position(row, col):
                target = board.get_piece(row, col)
                if target is None:
                    moves.append((row, col))
                elif target.color != self.color:
                    moves.append((row, col))
                    break
                else:
                    break
                row += dr
                col += dc
        
        return moves
    
    def can_reach(self, board: Board, from_row: int, from_col: int, 
                  to_row: int, to_col: int) -> bool:
        """Check if bishop can reach target position."""
        row_diff = to_row - from_row
        col_diff = to_col - from_col
        
        if abs(row_diff) != abs(col_diff):
            return False
        
        step_row = 1 if row_diff > 0 else -1
        step_col = 1 if col_diff > 0 else -1
        
        row, col = from_row + step_row, from_col + step_col
        while (row, col) != (to_row, to_col):
            if board.get_piece(row, col) is not None:
                return False
            row += step_row
            col += step_col
        
        target = board.get_piece(to_row, to_col)
        if target is None:
            return True
        return target.color != self.color


class Queen(Piece):
    """Queen piece - moves horizontally, vertically, and diagonally."""
    
    def __init__(self, color: str) -> None:
        super().__init__('♕' if color == 'white' else '♛', color)
    
    def get_valid_moves(self, board: Board, from_row: int, from_col: int) -> List[Tuple[int, int]]:
        """Get valid queen moves (all directions)."""
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), 
                      (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dr, dc in directions:
            row, col = from_row + dr, from_col + dc
            while board.is_valid_position(row, col):
                target = board.get_piece(row, col)
                if target is None:
                    moves.append((row, col))
                elif target.color != self.color:
                    moves.append((row, col))
                    break
                else:
                    break
                row += dr
                col += dc
        
        return moves
    
    def can_reach(self, board: Board, from_row: int, from_col: int, 
                  to_row: int, to_col: int) -> bool:
        """Check if queen can reach target position."""
        row_diff = to_row - from_row
        col_diff = to_col - from_col
        
        if row_diff == 0 or col_diff == 0:
            if row_diff == 0:
                step = 1 if col_diff > 0 else -1
                for col in range(from_col + step, to_col, step):
                    if board.get_piece(from_row, col) is not None:
                        return False
                return True
            
            if col_diff == 0:
                step = 1 if row_diff > 0 else -1
                for row in range(from_row + step, to_row, step):
                    if board.get_piece(row, from_col) is not None:
                        return False
                return True
        
        if abs(row_diff) == abs(col_diff):
            step_row = 1 if row_diff > 0 else -1
            step_col = 1 if col_diff > 0 else -1
            
            row, col = from_row + step_row, from_col + step_col
            while (row, col) != (to_row, to_col):
                if board.get_piece(row, col) is not None:
                    return False
                row += step_row
                col += step_col
            
            target = board.get_piece(to_row, to_col)
            if target is None:
                return True
            return target.color != self.color
        
        return False


class King(Piece):
    """King piece - moves one square in any direction."""
    
    def __init__(self, color: str) -> None:
        super().__init__('♔' if color == 'white' else '♚', color)
    
    def get_valid_moves(self, board: Board, from_row: int, from_col: int) -> List[Tuple[int, int]]:
        """Get valid king moves (one square in any direction)."""
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), 
                      (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dr, dc in directions:
            row, col = from_row + dr, from_col + dc
            if board.is_valid_position(row, col):
                target = board.get_piece(row, col)
                if target is None or target.color != self.color:
                    moves.append((row, col))
        
        return moves
    
    def can_reach(self, board: Board, from_row: int, from_col: int, 
                  to_row: int, to_col: int) -> bool:
        """Check if king can reach target position."""
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)
        
        if row_diff <= 1 and col_diff <= 1 and (row_diff != 0 or col_diff != 0):
            target = board.get_piece(to_row, to_col)
            if target is None:
                return True
            return target.color != self.color
        
        return False
