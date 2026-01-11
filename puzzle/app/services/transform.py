"""Coordinate transformation utilities."""

from typing import List, Tuple, Set


def normalize_coords(coords: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Normalize coordinates so minimum row and col are 0."""
    if not coords:
        return coords
    min_row = min(r for r, c in coords)
    min_col = min(c for r, c in coords)
    return [(r - min_row, c - min_col) for r, c in coords]


def rotate_coords_90_cw(coords: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Rotate coordinates 90 degrees clockwise around origin."""
    # (row, col) -> (col, -row)
    rotated = [(col, -row) for row, col in coords]
    return normalize_coords(rotated)


def rotate_coords_180(coords: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Rotate coordinates 180 degrees."""
    rotated = [(-row, -col) for row, col in coords]
    return normalize_coords(rotated)


def rotate_coords_270_cw(coords: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Rotate coordinates 270 degrees clockwise (90 counter-clockwise)."""
    rotated = [(-col, row) for row, col in coords]
    return normalize_coords(rotated)


def flip_horizontal(coords: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Flip coordinates horizontally (mirror across vertical axis)."""
    flipped = [(row, -col) for row, col in coords]
    return normalize_coords(flipped)


def flip_vertical(coords: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Flip coordinates vertically (mirror across horizontal axis)."""
    flipped = [(-row, col) for row, col in coords]
    return normalize_coords(flipped)


def get_all_orientations(base_coords: List[Tuple[int, int]]) -> List[List[Tuple[int, int]]]:
    """Get all unique orientations (rotations + flips) of a piece.

    Returns up to 8 unique orientations (4 rotations x 2 flip states).
    Symmetric pieces may have fewer unique orientations.
    """
    orientations = set()

    current = list(base_coords)
    for _ in range(4):  # 4 rotations
        # Add current rotation
        normalized = tuple(sorted(normalize_coords(current)))
        orientations.add(normalized)

        # Add flipped version
        flipped = flip_horizontal(current)
        normalized_flip = tuple(sorted(normalize_coords(flipped)))
        orientations.add(normalized_flip)

        # Rotate for next iteration
        current = rotate_coords_90_cw(current)

    return [list(o) for o in orientations]


def transform_piece(
    base_coords: List[Tuple[int, int]],
    rotation: int = 0,
    flipped: bool = False
) -> List[Tuple[int, int]]:
    """Apply rotation and flip to piece coordinates.

    Args:
        base_coords: Original piece coordinates
        rotation: Degrees clockwise (0, 90, 180, 270)
        flipped: Whether to flip horizontally

    Returns:
        Transformed and normalized coordinates
    """
    result = list(base_coords)

    # Apply flip first
    if flipped:
        result = flip_horizontal(result)

    # Apply rotation
    if rotation == 90:
        result = rotate_coords_90_cw(result)
    elif rotation == 180:
        result = rotate_coords_180(result)
    elif rotation == 270:
        result = rotate_coords_270_cw(result)

    return normalize_coords(result)
