"""Collision detection service."""

from typing import Set, Tuple, List
from dataclasses import dataclass

from app.models.game_state import GameState
from app.models.piece import PiecePlacement


@dataclass
class CollisionResult:
    """Result of a collision check."""
    is_valid: bool
    conflicts: List[Tuple[int, int]]  # Cells with other pieces
    out_of_bounds: List[Tuple[int, int]]  # Cells outside valid area
    obstructed: List[Tuple[int, int]]  # Cells blocked by plate obstructions


class CollisionService:
    """Service for checking piece placement validity."""

    def __init__(self, game_state: GameState):
        self.game_state = game_state

        # Cache computed values
        self._valid_cells = game_state.board_config.valid_cells
        self._obstructed_cells = game_state.get_obstructed_cells()
        self._occupied_cells = game_state.get_occupied_cells()

    def refresh_cache(self):
        """Refresh cached values after state changes."""
        self._occupied_cells = self.game_state.get_occupied_cells()

    def check_placement(self, placement: PiecePlacement) -> CollisionResult:
        """Check if a piece placement is valid."""
        piece_cells = set(placement.get_occupied_coords())

        conflicts = []
        out_of_bounds = []
        obstructed = []

        for cell in piece_cells:
            if cell not in self._valid_cells:
                out_of_bounds.append(cell)
            elif cell in self._obstructed_cells:
                obstructed.append(cell)
            elif cell in self._occupied_cells:
                conflicts.append(cell)

        is_valid = (len(conflicts) == 0 and
                    len(out_of_bounds) == 0 and
                    len(obstructed) == 0)

        return CollisionResult(
            is_valid=is_valid,
            conflicts=conflicts,
            out_of_bounds=out_of_bounds,
            obstructed=obstructed
        )

    def update_occupied(self, placement: PiecePlacement, add: bool = True):
        """Update occupied cells when placing/removing a piece."""
        piece_cells = set(placement.get_occupied_coords())
        if add:
            self._occupied_cells |= piece_cells
        else:
            self._occupied_cells -= piece_cells

    def get_valid_positions_for_piece(
        self,
        piece_id: str,
        rotation: int = 0,
        flipped: bool = False
    ) -> List[Tuple[int, int]]:
        """Get all valid anchor positions for a piece configuration."""
        from app.models.piece import PIECE_DEFINITIONS, PiecePlacement

        piece_def = PIECE_DEFINITIONS[piece_id]
        valid_positions = []

        # Try each possible anchor position
        for anchor in self._valid_cells:
            placement = PiecePlacement(
                piece_id=piece_id,
                anchor_position=anchor,
                rotation=rotation,
                flipped=flipped
            )

            result = self.check_placement(placement)
            if result.is_valid:
                valid_positions.append(anchor)

        return valid_positions
