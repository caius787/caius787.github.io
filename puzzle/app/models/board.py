"""Board configuration definitions."""

from dataclasses import dataclass
from typing import List, Tuple, Set, Dict
from enum import Enum


class BoardType(Enum):
    """Available board configurations."""
    # Basic configurations (edge-aligned)
    L_SHAPE = "L"
    REVERSE_L = "reverse_L"
    T_SHAPE = "T"
    I_SHAPE = "I"
    Z_SHAPE = "Z"
    REVERSE_Z = "reverse_Z"
    SQUARE = "square"
    # Offset configurations (2-dimple offset)
    PINWHEEL = "pinwheel"
    CROSS = "cross"
    Z_OFFSET = "z_offset"
    REVERSE_Z_OFFSET = "reverse_z_offset"


@dataclass
class PlatePosition:
    """Position of a plate within a board configuration."""
    plate_index: int  # Which plate slot (0-3)
    grid_offset: Tuple[int, int]  # (row, col) offset in dimple units


@dataclass
class BoardConfiguration:
    """Defines how 4 plates are arranged to form a board."""
    board_type: BoardType
    plate_positions: List[PlatePosition]
    total_width: int   # Total width in dimples
    total_height: int  # Total height in dimples
    valid_cells: Set[Tuple[int, int]]  # Set of valid (row, col) positions
    description: str = ""

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'type': self.board_type.value,
            'name': self.board_type.name.replace('_', ' ').title(),
            'description': self.description,
            'dimensions': [self.total_height, self.total_width],
            'plate_positions': [
                {'index': p.plate_index, 'offset': list(p.grid_offset)}
                for p in self.plate_positions
            ],
            'valid_cells': [list(c) for c in sorted(self.valid_cells)]
        }


class BoardBuilder:
    """Factory for creating board configurations."""

    # Plate offset definitions for each configuration
    # Each entry: list of (plate_index, row_offset, col_offset)
    CONFIGURATIONS: Dict[BoardType, dict] = {
        BoardType.SQUARE: {
            'positions': [(0, 0, 0), (1, 0, 4), (2, 4, 0), (3, 4, 4)],
            'width': 8, 'height': 8,
            'description': '2x2 grid of plates (8x8 dimples)'
        },
        BoardType.I_SHAPE: {
            'positions': [(0, 0, 0), (1, 0, 4), (2, 0, 8), (3, 0, 12)],
            'width': 16, 'height': 4,
            'description': '4 plates in a horizontal line (16x4 dimples)'
        },
        BoardType.L_SHAPE: {
            'positions': [(0, 0, 0), (1, 4, 0), (2, 4, 4), (3, 4, 8)],
            'width': 12, 'height': 8,
            'description': 'L-shape: 1 plate on top, 3 plates below'
        },
        BoardType.REVERSE_L: {
            'positions': [(0, 0, 8), (1, 4, 0), (2, 4, 4), (3, 4, 8)],
            'width': 12, 'height': 8,
            'description': 'Reverse L-shape: 1 plate top-right, 3 plates below'
        },
        BoardType.T_SHAPE: {
            'positions': [(0, 0, 0), (1, 0, 4), (2, 0, 8), (3, 4, 4)],
            'width': 12, 'height': 8,
            'description': 'T-shape: 3 plates on top, 1 plate centered below'
        },
        BoardType.Z_SHAPE: {
            'positions': [(0, 0, 0), (1, 0, 4), (2, 4, 4), (3, 4, 8)],
            'width': 12, 'height': 8,
            'description': 'Z-shape: 2 plates top-left, 2 plates bottom-right'
        },
        BoardType.REVERSE_Z: {
            'positions': [(0, 0, 4), (1, 0, 8), (2, 4, 0), (3, 4, 4)],
            'width': 12, 'height': 8,
            'description': 'Reverse Z-shape: 2 plates top-right, 2 plates bottom-left'
        },
        BoardType.PINWHEEL: {
            'positions': [(0, 0, 2), (1, 2, 6), (2, 6, 2), (3, 2, 0)],
            'width': 10, 'height': 10,
            'description': 'Pinwheel: 4 plates rotated around center with 2x2 hole',
            'hole': [(4, 4), (4, 5), (5, 4), (5, 5)]
        },
        BoardType.CROSS: {
            'positions': [(0, 0, 4), (1, 4, 0), (2, 4, 8), (3, 8, 4)],
            'width': 12, 'height': 12,
            'description': 'Cross: 4 plates arranged in a plus shape'
        },
        BoardType.Z_OFFSET: {
            'positions': [(0, 0, 0), (1, 0, 4), (2, 2, 4), (3, 2, 8)],
            'width': 12, 'height': 6,
            'description': 'Z with 2-dimple offset between rows'
        },
        BoardType.REVERSE_Z_OFFSET: {
            'positions': [(0, 0, 4), (1, 0, 8), (2, 2, 0), (3, 2, 4)],
            'width': 12, 'height': 6,
            'description': 'Reverse Z with 2-dimple offset between rows'
        },
    }

    @classmethod
    def build(cls, board_type: BoardType) -> BoardConfiguration:
        """Build a board configuration."""
        config = cls.CONFIGURATIONS[board_type]

        plate_positions = [
            PlatePosition(idx, (row, col))
            for idx, row, col in config['positions']
        ]

        # Calculate valid cells
        valid_cells = cls._calculate_valid_cells(
            config['positions'],
            config.get('hole', [])
        )

        return BoardConfiguration(
            board_type=board_type,
            plate_positions=plate_positions,
            total_width=config['width'],
            total_height=config['height'],
            valid_cells=valid_cells,
            description=config.get('description', '')
        )

    @classmethod
    def _calculate_valid_cells(
        cls,
        plate_positions: List[Tuple[int, int, int]],
        holes: List[Tuple[int, int]]
    ) -> Set[Tuple[int, int]]:
        """Calculate all valid cells for the board configuration."""
        valid = set()

        for _, row_offset, col_offset in plate_positions:
            # Each plate is 4x4
            for r in range(4):
                for c in range(4):
                    valid.add((row_offset + r, col_offset + c))

        # Remove holes
        for hole in holes:
            valid.discard(tuple(hole))

        return valid

    @classmethod
    def get_all_configurations(cls) -> List[BoardConfiguration]:
        """Get all available board configurations."""
        return [cls.build(bt) for bt in BoardType]
