"""Plate model definitions."""

from dataclasses import dataclass
from enum import Enum
from typing import Set, Tuple


class PlateSide(Enum):
    """Which side of the plate is facing up."""
    WHITE = "white"
    BLACK = "black"


def slot_to_coords(slot: int) -> Tuple[int, int]:
    """Convert 1-indexed slot to (row, col) 0-indexed coordinates.

    Slot numbering:
    | 1  2  3  4|
    | 5  6  7  8|
    | 9 10 11 12|
    |13 14 15 16|
    """
    slot_0 = slot - 1
    return (slot_0 // 4, slot_0 % 4)


def coords_to_slot(row: int, col: int) -> int:
    """Convert (row, col) to 1-indexed slot number."""
    return row * 4 + col + 1


@dataclass
class PlateDefinition:
    """Static plate obstruction definitions."""
    plate_id: int
    white_obstructions: Set[int]  # Slot numbers blocked on white side
    black_obstructions: Set[int]  # Slot numbers blocked on black side


@dataclass
class PlateInstance:
    """A plate placed on the board with orientation."""
    definition: PlateDefinition
    side: PlateSide = PlateSide.WHITE
    rotation: int = 0  # 0, 90, 180, or 270 degrees clockwise
    position: Tuple[int, int] = (0, 0)  # Board grid position (row, col offset)

    def get_obstructions(self) -> Set[int]:
        """Get obstructions for current side, transformed by rotation."""
        base = (self.definition.white_obstructions
                if self.side == PlateSide.WHITE
                else self.definition.black_obstructions)
        return self._apply_rotation(base)

    def _apply_rotation(self, slots: Set[int]) -> Set[int]:
        """Rotate slot positions by current rotation."""
        if self.rotation == 0:
            return slots
        return {self._rotate_slot(s) for s in slots}

    def _rotate_slot(self, slot: int) -> int:
        """Rotate a single slot position."""
        row, col = slot_to_coords(slot)
        if self.rotation == 90:
            new_row, new_col = col, 3 - row
        elif self.rotation == 180:
            new_row, new_col = 3 - row, 3 - col
        elif self.rotation == 270:
            new_row, new_col = 3 - col, row
        else:
            new_row, new_col = row, col
        return coords_to_slot(new_row, new_col)

    def get_global_obstructions(self) -> Set[Tuple[int, int]]:
        """Get obstructed cells in global board coordinates."""
        obstructed = set()
        for slot in self.get_obstructions():
            row, col = slot_to_coords(slot)
            global_row = self.position[0] + row
            global_col = self.position[1] + col
            obstructed.add((global_row, global_col))
        return obstructed

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'plate_id': self.definition.plate_id,
            'side': self.side.value,
            'rotation': self.rotation,
            'position': list(self.position),
            'obstructions': [list(slot_to_coords(s)) for s in self.get_obstructions()],
            'global_obstructions': [list(pos) for pos in self.get_global_obstructions()]
        }


# Static plate definitions
# White side obstructions: P1(1,4), P2(14,15), P3(2), P4(2,16)
# Black side obstructions: P1(8,16), P2(4,11), P3(3), P4(7,16)
PLATE_DEFINITIONS = {
    1: PlateDefinition(1, white_obstructions={1, 4}, black_obstructions={8, 16}),
    2: PlateDefinition(2, white_obstructions={14, 15}, black_obstructions={4, 11}),
    3: PlateDefinition(3, white_obstructions={2}, black_obstructions={3}),
    4: PlateDefinition(4, white_obstructions={2, 16}, black_obstructions={7, 16}),
}
