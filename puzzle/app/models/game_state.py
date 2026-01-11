"""Game state management."""

from dataclasses import dataclass, field
from typing import Dict, Set, Tuple, List, Optional
import uuid

from .board import BoardConfiguration, BoardType, BoardBuilder
from .plate import PlateInstance, PlateDefinition, PlateSide, PLATE_DEFINITIONS
from .piece import PiecePlacement, PIECE_DEFINITIONS


@dataclass
class GameState:
    """Complete state of a puzzle game."""
    game_id: str
    board_config: BoardConfiguration
    plates: List[PlateInstance]  # 4 plates with their orientations
    placed_pieces: Dict[str, PiecePlacement] = field(default_factory=dict)
    available_pieces: Set[str] = field(default_factory=set)

    def __post_init__(self):
        if not self.available_pieces:
            self.available_pieces = set(PIECE_DEFINITIONS.keys())

    def get_obstructed_cells(self) -> Set[Tuple[int, int]]:
        """Get all cells blocked by plate obstructions."""
        obstructed = set()
        for plate in self.plates:
            obstructed.update(plate.get_global_obstructions())
        return obstructed

    def get_occupied_cells(self) -> Set[Tuple[int, int]]:
        """Get all cells occupied by placed pieces."""
        occupied = set()
        for placement in self.placed_pieces.values():
            occupied.update(placement.get_occupied_coords())
        return occupied

    def get_available_cells(self) -> Set[Tuple[int, int]]:
        """Get cells that can receive pieces."""
        valid = self.board_config.valid_cells
        obstructed = self.get_obstructed_cells()
        occupied = self.get_occupied_cells()
        return valid - obstructed - occupied

    def is_solved(self) -> bool:
        """Check if puzzle is complete (all pieces placed)."""
        return len(self.available_pieces) == 0

    def place_piece(self, placement: PiecePlacement) -> bool:
        """Attempt to place a piece. Returns True if successful."""
        piece_id = placement.piece_id

        # Check piece is available
        if piece_id not in self.available_pieces:
            return False

        # Check all cells are valid
        cells = set(placement.get_occupied_coords())
        available = self.get_available_cells()

        if not cells.issubset(available):
            return False

        # Place the piece
        self.placed_pieces[piece_id] = placement
        self.available_pieces.remove(piece_id)
        return True

    def remove_piece(self, piece_id: str) -> bool:
        """Remove a placed piece. Returns True if successful."""
        if piece_id not in self.placed_pieces:
            return False

        del self.placed_pieces[piece_id]
        self.available_pieces.add(piece_id)
        return True

    def validate_placement(self, placement: PiecePlacement) -> dict:
        """Check if a placement is valid and return details."""
        piece_id = placement.piece_id
        cells = set(placement.get_occupied_coords())

        result = {
            'valid': True,
            'conflicts': [],
            'out_of_bounds': [],
            'obstructed': [],
            'piece_unavailable': False
        }

        # Check piece availability
        if piece_id not in self.available_pieces:
            result['valid'] = False
            result['piece_unavailable'] = True
            return result

        valid_cells = self.board_config.valid_cells
        obstructed = self.get_obstructed_cells()
        occupied = self.get_occupied_cells()

        for cell in cells:
            if cell not in valid_cells:
                result['out_of_bounds'].append(list(cell))
                result['valid'] = False
            elif cell in obstructed:
                result['obstructed'].append(list(cell))
                result['valid'] = False
            elif cell in occupied:
                result['conflicts'].append(list(cell))
                result['valid'] = False

        return result

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'game_id': self.game_id,
            'board_config': self.board_config.to_dict(),
            'plates': [p.to_dict() for p in self.plates],
            'placed_pieces': {k: v.to_dict() for k, v in self.placed_pieces.items()},
            'available_pieces': list(self.available_pieces),
            'obstructed_cells': [list(c) for c in sorted(self.get_obstructed_cells())],
            'occupied_cells': [list(c) for c in sorted(self.get_occupied_cells())],
            'available_cells': [list(c) for c in sorted(self.get_available_cells())],
            'is_solved': self.is_solved()
        }

    @classmethod
    def create_new_game(
        cls,
        board_type: BoardType,
        plate_configs: Optional[List[dict]] = None
    ) -> 'GameState':
        """Create a new game with specified board and plate configurations."""
        board_config = BoardBuilder.build(board_type)
        game_id = str(uuid.uuid4())[:8]

        # Default plate configurations if not provided
        if plate_configs is None:
            plate_configs = [
                {'plate_id': i + 1, 'side': 'white', 'rotation': 0}
                for i in range(4)
            ]

        plates = []
        for i, config in enumerate(plate_configs):
            plate_id = config.get('plate_id', i + 1)
            plate_def = PLATE_DEFINITIONS[plate_id]

            side_str = config.get('side', 'white')
            side = PlateSide.WHITE if side_str == 'white' else PlateSide.BLACK

            plate = PlateInstance(
                definition=plate_def,
                side=side,
                rotation=config.get('rotation', 0),
                position=board_config.plate_positions[i].grid_offset
            )
            plates.append(plate)

        return cls(
            game_id=game_id,
            board_config=board_config,
            plates=plates,
            placed_pieces={},
            available_pieces=set(PIECE_DEFINITIONS.keys())
        )


# In-memory game storage
_games: Dict[str, GameState] = {}


def get_game(game_id: str) -> Optional[GameState]:
    """Get a game by ID."""
    return _games.get(game_id)


def save_game(game: GameState) -> None:
    """Save a game."""
    _games[game.game_id] = game


def delete_game(game_id: str) -> bool:
    """Delete a game."""
    if game_id in _games:
        del _games[game_id]
        return True
    return False
