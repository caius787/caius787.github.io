# Puzzle Game

A web-based puzzle game where players arrange 12 uniquely-shaped pieces onto a configurable game board. The board is formed by connecting 4 two-sided plates, each with obstructions that add strategic complexity.

## Features

- **11 Board Configurations** - L, T, I, Z shapes, Square, Pinwheel, Cross, and more
- **4 Configurable Plates** - Each plate is two-sided (white/black) with different obstruction patterns
- **12 Unique Pieces** - Each piece has a distinct shape and color
- **Piece Manipulation** - Rotate and flip pieces to find the right fit
- **Drag-and-Drop Plate Swapping** - Easily rearrange plate positions
- **Auto-Solver** - Watch the computer solve the puzzle with animated piece placement
- **Hint System** - Get suggestions for your next move

## Installation

### Prerequisites

- Python 3.8 or higher

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/puzzle.git
   cd puzzle
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Game

1. Start the server:
   ```bash
   python run.py
   ```

2. Open your browser to [http://localhost:5001](http://localhost:5001)

## How to Play

### Setup

1. Select a board configuration from the dropdown
2. Configure each plate's side (white/black) and rotation as desired
3. Drag plate cards to swap their positions in the layout

### Placing Pieces

1. Click a piece in the sidebar to select it
2. Move your mouse over the board to preview placement
3. Press **R** to rotate the piece 90°
4. Press **F** to flip the piece
5. Click on the board to place the piece
6. Press **Esc** to cancel selection

### Controls

| Action | Control |
|--------|---------|
| Select piece | Click piece in sidebar |
| Place piece | Click on board |
| Rotate piece | **R** key or right-click |
| Flip piece | **F** key |
| Cancel selection | **Esc** key |
| Remove piece | Click placed piece on board |

### Buttons

- **New Game** - Start a fresh game with current board configuration
- **Auto Solve** - Let the computer solve the puzzle
- **Hint** - Get a suggestion for the next piece
- **Reset** - Remove all placed pieces

## Project Structure

```
puzzle/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── models/
│   │   ├── plate.py          # Plate definitions and obstructions
│   │   ├── piece.py          # Piece shape definitions
│   │   ├── board.py          # Board configuration layouts
│   │   └── game_state.py     # Game state management
│   ├── services/
│   │   ├── solver.py         # Auto-solver algorithm
│   │   ├── collision.py      # Placement validation
│   │   └── transform.py      # Rotation/flip utilities
│   └── routes/
│       ├── game.py           # Game API endpoints
│       ├── solver.py         # Solver API endpoints
│       └── board.py          # Board/piece info endpoints
├── static/
│   ├── css/style.css         # Game styling
│   └── js/
│       ├── main.js           # Application logic
│       ├── renderer.js       # Canvas rendering
│       ├── interactions.js   # User input handling
│       └── api.js            # Backend API calls
├── templates/
│   └── index.html            # Game page
├── run.py                    # Application entry point
├── requirements.txt          # Python dependencies
├── GAME_RULES.md            # Detailed game rules
└── ORIGINAL_INSTRUCTIONS.md  # Original project specifications
```

## Technology Stack

- **Backend**: Python, Flask
- **Frontend**: Vanilla JavaScript, HTML5 Canvas
- **Styling**: CSS3

## Solver Algorithm

The auto-solver uses a backtracking algorithm with constraint satisfaction:

- **MRV Heuristic** - Places most constrained pieces first
- **Forward Checking** - Prunes branches where remaining pieces can't fit
- **Pre-computation** - Calculates valid placements before solving

## License

MIT License
