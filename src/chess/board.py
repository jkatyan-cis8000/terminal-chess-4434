from typing import Tuple, Optional, List, TYPE_CHECKING
import copy

if TYPE_CHECKING:
    from .pieces import Piece


class Board:
    """8x8 chess board with piece positioning."""
    
    def __init__(self) -> None:
        """Initialize empty 8x8 board."""
        self._grid: List[List[Optional[Piece]]] = [[None for _ in range(8)] for _ in range(8)]
    
    def get_piece(self, row: int, col: int) -> Optional['Piece']:
        """Get piece at position (row, col)."""
        if not self.is_valid_position(row, col):
            raise ValueError(f"Invalid position: ({row}, {col})")
        return self._grid[row][col]
    
    def set_piece(self, row: int, col: int, piece: Optional['Piece']) -> None:
        """Set piece at position (row, col)."""
        if not self.is_valid_position(row, col):
            raise ValueError(f"Invalid position: ({row}, {col})")
        self._grid[row][col] = piece
    
    def copy(self) -> 'Board':
        """Create deep copy of board."""
        new_board = Board()
        new_board._grid = [[piece if piece is None else copy.copy(piece) for piece in row] for row in self._grid]
        return new_board
    
    def is_valid_position(self, row: int, col: int) -> bool:
        """Check if position is within board bounds."""
        return 0 <= row < 8 and 0 <= col < 8
