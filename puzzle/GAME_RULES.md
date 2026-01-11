# Puzzle Game Rules and Specifications

## Overview

A tile-based puzzle game where players arrange 12 uniquely-shaped pieces onto a game board formed by connecting 4 two-sided plates. The objective is to fill all open dimples while avoiding obstructions.

---

## Components

### Plates

- **Quantity:** 4 plates total
- **Surface:** Each plate has a 4x4 grid of dimples (16 slots per plate)
- **Two-sided:** Each plate has a white side and a black side
- **Obstructions:** Each side has 1-2 obstructions that prevent pieces from being placed in those slots
  - White obstructions appear on the black side
  - Black obstructions appear on the white side
- **Rotatable:** Each plate can be rotated in 90-degree increments (0°, 90°, 180°, 270°)
- **Connectable:** Plates connect edge-to-edge with other plates

### Slot Numbering

Each plate's 4x4 grid uses the following slot numbering:

```
|  1   2   3   4 |
|  5   6   7   8 |
|  9  10  11  12 |
| 13  14  15  16 |
```

### Obstruction Locations

**White Side Obstructions:**
- Plate 1: Slots 1, 4
- Plate 2: Slots 14, 15
- Plate 3: Slot 2
- Plate 4: Slots 2, 16

**Black Side Obstructions:**
- Plate 1: Slots 8, 16
- Plate 2: Slots 4, 11
- Plate 3: Slot 3
- Plate 4: Slots 7, 16

---

## Board Configurations

The 4 plates can be arranged into 11 different board shapes:

### Basic Configurations (Edge-Aligned)

1. **L-Shape** - 1 plate on top, 3 plates in a row below
2. **Reverse L-Shape** - Mirror of L-shape
3. **T-Shape** - 3 plates in a row on top, 1 plate centered below
4. **I-Shape** - 4 plates in a horizontal line
5. **Z-Shape** - 2 plates top-left, 2 plates bottom-right (offset)
6. **Reverse Z-Shape** - Mirror of Z-shape
7. **Square** - 2x2 grid of plates

### Offset Configurations (2-Dimple Offset)

8. **Pinwheel** - 4 plates arranged around a 2x2 hole in the center
9. **Cross** - 4 plates arranged in a plus/cross pattern
10. **Z-Offset** - Z-shape with 2-dimple vertical offset between rows
11. **Reverse Z-Offset** - Mirror of Z-offset

---

## Piece Shapes

All pieces are composed of balls that fit into the dimples. There are 12 pieces total, each with a unique shape and color.

### Piece Definitions

Each piece is defined by which slots it occupies on a 4x4 reference grid:

| Color | Slots | Ball Count |
|-------|-------|------------|
| Dark Red | 1, 2, 6, 7 | 4 |
| Light Red | 1, 2, 3, 4, 8 | 5 |
| Orange | 1, 5, 6, 7, 10 | 5 |
| Yellow | 1, 2, 3, 4, 7 | 5 |
| Lime Green | 1, 2, 3, 5, 7 | 5 |
| Turquoise | 1, 2, 3, 5, 6 | 5 |
| Dark Green | 1, 2, 3, 6, 10 | 5 |
| Light Blue | 1, 2, 5 | 3 |
| Blue | 1, 2, 3, 5, 9 | 5 |
| Dark Blue | 1, 5, 6, 7, 11 | 5 |
| Purple | 1, 2, 6, 7, 11 | 5 |
| Pink | 1, 2, 3, 7, 8 | 5 |

### Piece Properties

- All pieces can be **rotated** (0°, 90°, 180°, 270°)
- All pieces can be **flipped** (mirrored)
- Pieces can span across plate borders
- Piece shapes are fixed and cannot be modified

---

## Game Rules

### Setup

1. Choose one of the 11 board configurations
2. Arrange the 4 plates according to the chosen configuration
3. For each plate, choose which side faces up (white or black)
4. Optionally rotate individual plates

### Gameplay

1. Select a piece from the available pieces
2. Rotate or flip the piece as needed
3. Place the piece on the board so all balls fit into dimples
4. Repeat until all pieces are placed or no valid moves remain

### Placement Rules

- A piece **cannot** be placed on an obstruction
- A piece **cannot** overlap with another placed piece
- All balls of a piece **must** fit within valid dimple positions
- Pieces **can** span across multiple plates

### Victory Condition

The puzzle is solved when all 12 pieces have been successfully placed on the board with no overlaps and no pieces on obstructions.

---

## Strategy Tips

- Start with the most constrained pieces (those with fewer valid placement options)
- Consider obstruction locations when choosing plate sides and rotations
- Larger pieces are often harder to place later in the game
- The 3-ball piece (Light Blue) is the most flexible and can often fill gaps

---

## Total Ball Count

The 12 pieces contain a total of **57 balls** that must fit into the available dimples on the board (64 total dimples minus obstructions).
