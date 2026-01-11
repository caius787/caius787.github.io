"""Puzzle solver using backtracking with constraint satisfaction."""

from typing import List, Set, Tuple, Optional, Dict
from dataclasses import dataclass, field
import time
import copy

from app.models.game_state import GameState
from app.models.piece import PieceDefinition, PiecePlacement, PIECE_DEFINITIONS


@dataclass
class SolverStats:
    """Statistics about the solving process."""
    nodes_explored: int = 0
    solutions_found: int = 0
    time_elapsed_ms: float = 0
    pruned_branches: int = 0


@dataclass
class SolverResult:
    """Result of a solve attempt."""
    success: bool
    solution: Optional[List[PiecePlacement]] = None
    stats: SolverStats = field(default_factory=SolverStats)
    message: str = ""


class PuzzleSolver:
    """Backtracking solver with constraint propagation."""

    def __init__(self, game_state: GameState, timeout_seconds: float = 30.0):
        self.game_state = game_state
        self.timeout = timeout_seconds
        self.stats = SolverStats()
        self.start_time = None

        # Pre-compute valid placements for each piece
        self.valid_placements = self._precompute_placements()

    def _precompute_placements(self) -> Dict[str, List[PiecePlacement]]:
        """Pre-compute all valid placements for each piece."""
        placements = {}
        valid_cells = self.game_state.board_config.valid_cells
        obstructed = self.game_state.get_obstructed_cells()
        available = valid_cells - obstructed

        for piece_id in self.game_state.available_pieces:
            piece_def = PIECE_DEFINITIONS[piece_id]
            placements[piece_id] = []

            # Try all rotations and flips
            seen_orientations = set()

            for rotation in [0, 90, 180, 270]:
                for flipped in [False, True]:
                    # Create a test placement to get the shape
                    test_placement = PiecePlacement(
                        piece_id=piece_id,
                        anchor_position=(0, 0),
                        rotation=rotation,
                        flipped=flipped
                    )

                    # Get the relative shape for this orientation
                    rel_coords = test_placement._transform_coords(
                        piece_def.get_relative_coords()
                    )
                    orientation_key = tuple(sorted(rel_coords))

                    # Skip if we've seen this orientation
                    if orientation_key in seen_orientations:
                        continue
                    seen_orientations.add(orientation_key)

                    # Try all anchor positions
                    for anchor in available:
                        placement = PiecePlacement(
                            piece_id=piece_id,
                            anchor_position=anchor,
                            rotation=rotation,
                            flipped=flipped
                        )

                        # Check if placement is valid (within bounds, no obstructions)
                        occupied = set(placement.get_occupied_coords())

                        # All cells must be valid and not obstructed
                        if occupied.issubset(available):
                            placements[piece_id].append(placement)

        return placements

    def solve(self) -> SolverResult:
        """Main solving entry point."""
        self.start_time = time.time()
        self.stats = SolverStats()

        # Check if already solved
        if self.game_state.is_solved():
            return SolverResult(
                success=True,
                solution=[],
                stats=self.stats,
                message="Puzzle already solved"
            )

        # Get available cells (excluding obstructions and already placed pieces)
        available_cells = self.game_state.get_available_cells()

        if not available_cells:
            return SolverResult(
                success=False,
                stats=self.stats,
                message="No available cells"
            )

        # Sort pieces by constrainedness (MRV heuristic)
        pieces = self._order_pieces_by_mrv()

        if not pieces:
            return SolverResult(
                success=True,
                solution=[],
                stats=self.stats,
                message="No pieces to place"
            )

        # Start backtracking
        solution = self._backtrack(
            pieces=pieces,
            placed=[],
            occupied_cells=self.game_state.get_occupied_cells(),
            available_cells=available_cells
        )

        self.stats.time_elapsed_ms = (time.time() - self.start_time) * 1000

        if solution is not None:
            return SolverResult(
                success=True,
                solution=solution,
                stats=self.stats,
                message=f"Solution found in {self.stats.time_elapsed_ms:.0f}ms"
            )
        else:
            return SolverResult(
                success=False,
                stats=self.stats,
                message="No solution found (timeout or unsolvable)"
            )

    def _order_pieces_by_mrv(self) -> List[str]:
        """Order pieces by Minimum Remaining Values heuristic."""
        # Pieces with fewer valid placements should be tried first
        piece_counts = [
            (piece_id, len(self.valid_placements.get(piece_id, [])))
            for piece_id in self.game_state.available_pieces
        ]
        piece_counts.sort(key=lambda x: x[1])
        return [piece_id for piece_id, _ in piece_counts]

    def _backtrack(
        self,
        pieces: List[str],
        placed: List[PiecePlacement],
        occupied_cells: Set[Tuple[int, int]],
        available_cells: Set[Tuple[int, int]]
    ) -> Optional[List[PiecePlacement]]:
        """Recursive backtracking with constraint propagation."""

        # Check timeout
        if time.time() - self.start_time > self.timeout:
            return None

        self.stats.nodes_explored += 1

        # Base case: all pieces placed
        if not pieces:
            self.stats.solutions_found += 1
            return placed.copy()

        # Select next piece (first in MRV-ordered list)
        piece_id = pieces[0]
        remaining_pieces = pieces[1:]

        # Get valid placements for this piece given current state
        for placement in self.valid_placements.get(piece_id, []):
            piece_cells = set(placement.get_occupied_coords())

            # Check for collision with already placed pieces
            if piece_cells & occupied_cells:
                continue

            # Check if all cells are still available
            if not piece_cells.issubset(available_cells):
                continue

            # Forward checking: prune if any remaining piece becomes unplaceable
            new_occupied = occupied_cells | piece_cells
            new_available = available_cells - piece_cells

            if self._forward_check(remaining_pieces, new_available, new_occupied):
                # Place piece and recurse
                placed.append(placement)

                result = self._backtrack(
                    pieces=remaining_pieces,
                    placed=placed,
                    occupied_cells=new_occupied,
                    available_cells=new_available
                )

                if result is not None:
                    return result

                # Backtrack
                placed.pop()
            else:
                self.stats.pruned_branches += 1

        return None

    def _forward_check(
        self,
        remaining_pieces: List[str],
        available_cells: Set[Tuple[int, int]],
        occupied_cells: Set[Tuple[int, int]]
    ) -> bool:
        """Check if all remaining pieces have at least one valid placement."""
        for piece_id in remaining_pieces:
            has_valid = False

            for placement in self.valid_placements.get(piece_id, []):
                piece_cells = set(placement.get_occupied_coords())

                if (not (piece_cells & occupied_cells) and
                        piece_cells.issubset(available_cells)):
                    has_valid = True
                    break

            if not has_valid:
                return False

        return True

    def get_hint(self) -> Optional[PiecePlacement]:
        """Get a hint for the next piece to place."""
        pieces = self._order_pieces_by_mrv()
        if not pieces:
            return None

        # Try to find any valid placement for the most constrained piece
        piece_id = pieces[0]
        occupied = self.game_state.get_occupied_cells()
        available = self.game_state.get_available_cells()

        for placement in self.valid_placements.get(piece_id, []):
            piece_cells = set(placement.get_occupied_coords())
            if (not (piece_cells & occupied) and
                    piece_cells.issubset(available)):
                return placement

        return None

    def check_solvable(self) -> Tuple[bool, str]:
        """Quick check if puzzle appears solvable."""
        # Count available cells
        available = self.game_state.get_available_cells()
        total_cells_needed = sum(
            len(PIECE_DEFINITIONS[p].base_slots)
            for p in self.game_state.available_pieces
        )

        if len(available) < total_cells_needed:
            return False, f"Not enough cells: {len(available)} available, {total_cells_needed} needed"

        # Check each piece has at least one valid placement
        for piece_id in self.game_state.available_pieces:
            if not self.valid_placements.get(piece_id):
                return False, f"No valid placement for {piece_id}"

        return True, "Puzzle appears solvable"
