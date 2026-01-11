"""Piece model definitions."""

from dataclasses import dataclass
from typing import Tuple, List, Set
from .plate import slot_to_coords


@dataclass
class PieceDefinition:
    """Static piece shape definitions."""
    piece_id: str
    name: str
    color: str  # Hex color code
    base_slots: Tuple[int, ...]  # Original slot pattern

    def get_relative_coords(self) -> List[Tuple[int, int]]:
        """Convert slots to relative (row, col) offsets from anchor."""
        coords = [slot_to_coords(s) for s in self.base_slots]
        # Normalize: make minimum row and col be 0
        min_row = min(c[0] for c in coords)
        min_col = min(c[1] for c in coords)
        return [(r - min_row, c - min_col) for r, c in coords]

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.piece_id,
            'name': self.name,
            'color': self.color,
            'slots': list(self.base_slots),
            'cell_count': len(self.base_slots),
            'shape': self.get_relative_coords()
        }


@dataclass
class PiecePlacement:
    """A piece placed on the board."""
    piece_id: str
    anchor_position: Tuple[int, int]  # Global board (row, col)
    rotation: int = 0  # 0, 90, 180, 270
    flipped: bool = False

    def get_occupied_coords(self) -> List[Tuple[int, int]]:
        """Get all board coordinates occupied by this placement."""
        piece_def = PIECE_DEFINITIONS[self.piece_id]
        base = piece_def.get_relative_coords()
        transformed = self._transform_coords(base)
        return [(r + self.anchor_position[0], c + self.anchor_position[1])
                for r, c in transformed]

    def _transform_coords(self, coords: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """Apply rotation and flip to relative coordinates."""
        result = list(coords)

        # Apply flip first (mirror across vertical axis)
        if self.flipped:
            result = [(r, -c) for r, c in result]

        # Apply rotation (clockwise)
        for _ in range(self.rotation // 90):
            result = [(c, -r) for r, c in result]

        # Normalize to positive coordinates
        if result:
            min_row = min(r for r, c in result)
            min_col = min(c for r, c in result)
            result = [(r - min_row, c - min_col) for r, c in result]

        return result

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'piece_id': self.piece_id,
            'anchor_position': list(self.anchor_position),
            'rotation': self.rotation,
            'flipped': self.flipped,
            'occupied_coords': [list(c) for c in self.get_occupied_coords()]
        }


# Static piece definitions
# All pieces defined by slot numbers on a 4x4 grid
PIECE_DEFINITIONS = {
    'dark_red': PieceDefinition('dark_red', 'Dark Red', '#8B0000', (1, 2, 6, 7)),
    'light_red': PieceDefinition('light_red', 'Light Red', '#FF6B6B', (1, 2, 3, 4, 8)),
    'orange': PieceDefinition('orange', 'Orange', '#FFA500', (1, 5, 6, 7, 10)),
    'yellow': PieceDefinition('yellow', 'Yellow', '#FFD700', (1, 2, 3, 4, 7)),
    'lime_green': PieceDefinition('lime_green', 'Lime Green', '#32CD32', (1, 2, 3, 5, 7)),
    'turquoise': PieceDefinition('turquoise', 'Turquoise', '#40E0D0', (1, 2, 3, 5, 6)),
    'dark_green': PieceDefinition('dark_green', 'Dark Green', '#006400', (1, 2, 3, 6, 10)),
    'light_blue': PieceDefinition('light_blue', 'Light Blue', '#87CEEB', (1, 2, 5)),
    'blue': PieceDefinition('blue', 'Blue', '#0000FF', (1, 2, 3, 5, 9)),
    'dark_blue': PieceDefinition('dark_blue', 'Dark Blue', '#00008B', (1, 5, 6, 7, 11)),
    'purple': PieceDefinition('purple', 'Purple', '#800080', (1, 2, 6, 7, 11)),
    'pink': PieceDefinition('pink', 'Pink', '#FF69B4', (1, 2, 3, 7, 8)),
}
