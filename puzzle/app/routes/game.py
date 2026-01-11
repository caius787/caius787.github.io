"""Game state API endpoints."""

from flask import Blueprint, request, jsonify

from app.models.board import BoardType
from app.models.game_state import GameState, get_game, save_game, delete_game
from app.models.piece import PiecePlacement

game_bp = Blueprint('game', __name__, url_prefix='/api/game')


@game_bp.route('/new', methods=['POST'])
def create_game():
    """
    Create a new game with specified configuration.

    Request body:
    {
        "board_type": "square",
        "plates": [
            {"plate_id": 1, "side": "white", "rotation": 0},
            {"plate_id": 2, "side": "white", "rotation": 0},
            {"plate_id": 3, "side": "white", "rotation": 0},
            {"plate_id": 4, "side": "white", "rotation": 0}
        ]
    }
    """
    data = request.get_json() or {}

    board_type_str = data.get('board_type', 'square')

    # Convert string to BoardType enum
    try:
        board_type = BoardType(board_type_str)
    except ValueError:
        # Try uppercase
        try:
            board_type = BoardType[board_type_str.upper()]
        except KeyError:
            return jsonify({
                'error': f'Invalid board type: {board_type_str}',
                'valid_types': [bt.value for bt in BoardType]
            }), 400

    plate_configs = data.get('plates')

    try:
        game = GameState.create_new_game(board_type, plate_configs)
        save_game(game)

        return jsonify({
            'game_id': game.game_id,
            'state': game.to_dict()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@game_bp.route('/<game_id>/state', methods=['GET'])
def get_state(game_id):
    """Get current game state."""
    game = get_game(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404

    return jsonify({'state': game.to_dict()})


@game_bp.route('/<game_id>/place', methods=['POST'])
def place_piece(game_id):
    """
    Place a piece on the board.

    Request body:
    {
        "piece_id": "dark_red",
        "position": [2, 3],
        "rotation": 90,
        "flipped": false
    }
    """
    game = get_game(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    piece_id = data.get('piece_id')
    position = data.get('position', [0, 0])
    rotation = data.get('rotation', 0)
    flipped = data.get('flipped', False)

    if not piece_id:
        return jsonify({'error': 'piece_id is required'}), 400

    placement = PiecePlacement(
        piece_id=piece_id,
        anchor_position=tuple(position),
        rotation=rotation,
        flipped=flipped
    )

    # Validate first
    validation = game.validate_placement(placement)
    if not validation['valid']:
        return jsonify({
            'success': False,
            'validation': validation,
            'state': game.to_dict()
        })

    # Place the piece
    success = game.place_piece(placement)
    save_game(game)

    return jsonify({
        'success': success,
        'state': game.to_dict(),
        'is_solved': game.is_solved()
    })


@game_bp.route('/<game_id>/remove', methods=['POST'])
def remove_piece(game_id):
    """
    Remove a placed piece from the board.

    Request body:
    {
        "piece_id": "dark_red"
    }
    """
    game = get_game(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404

    data = request.get_json()
    piece_id = data.get('piece_id') if data else None

    if not piece_id:
        return jsonify({'error': 'piece_id is required'}), 400

    success = game.remove_piece(piece_id)
    if success:
        save_game(game)

    return jsonify({
        'success': success,
        'state': game.to_dict()
    })


@game_bp.route('/<game_id>/validate', methods=['POST'])
def validate_placement(game_id):
    """
    Validate if a piece can be placed at position.

    Request body:
    {
        "piece_id": "orange",
        "position": [0, 4],
        "rotation": 0,
        "flipped": false
    }
    """
    game = get_game(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    piece_id = data.get('piece_id')
    position = data.get('position', [0, 0])
    rotation = data.get('rotation', 0)
    flipped = data.get('flipped', False)

    if not piece_id:
        return jsonify({'error': 'piece_id is required'}), 400

    placement = PiecePlacement(
        piece_id=piece_id,
        anchor_position=tuple(position),
        rotation=rotation,
        flipped=flipped
    )

    validation = game.validate_placement(placement)

    return jsonify({
        'validation': validation,
        'occupied_coords': [list(c) for c in placement.get_occupied_coords()]
    })


@game_bp.route('/<game_id>/reset', methods=['POST'])
def reset_game(game_id):
    """Reset game to initial state (remove all placed pieces)."""
    game = get_game(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404

    # Remove all placed pieces
    from app.models.piece import PIECE_DEFINITIONS
    game.placed_pieces = {}
    game.available_pieces = set(PIECE_DEFINITIONS.keys())
    save_game(game)

    return jsonify({
        'success': True,
        'state': game.to_dict()
    })


@game_bp.route('/<game_id>/rotate-plate', methods=['POST'])
def rotate_plate(game_id):
    """
    Rotate a plate or flip it to the other side.

    Request body:
    {
        "plate_index": 0,
        "rotation": 90,  // optional
        "flip": true     // optional - flip to other side
    }
    """
    game = get_game(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    plate_index = data.get('plate_index')
    if plate_index is None or plate_index < 0 or plate_index >= len(game.plates):
        return jsonify({'error': 'Invalid plate_index'}), 400

    plate = game.plates[plate_index]

    if 'rotation' in data:
        rotation = data['rotation']
        if rotation not in [0, 90, 180, 270]:
            return jsonify({'error': 'Invalid rotation (must be 0, 90, 180, or 270)'}), 400
        plate.rotation = rotation

    if data.get('flip'):
        from app.models.plate import PlateSide
        plate.side = (PlateSide.BLACK if plate.side == PlateSide.WHITE
                      else PlateSide.WHITE)

    save_game(game)

    return jsonify({
        'success': True,
        'state': game.to_dict()
    })


@game_bp.route('/<game_id>/swap-plates', methods=['POST'])
def swap_plates(game_id):
    """
    Swap two plates in the layout.

    Request body:
    {
        "from_index": 0,
        "to_index": 1
    }
    """
    game = get_game(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    from_index = data.get('from_index')
    to_index = data.get('to_index')

    if from_index is None or to_index is None:
        return jsonify({'error': 'from_index and to_index are required'}), 400

    if (from_index < 0 or from_index >= len(game.plates) or
            to_index < 0 or to_index >= len(game.plates)):
        return jsonify({'error': 'Invalid plate index'}), 400

    if from_index == to_index:
        return jsonify({'success': True, 'state': game.to_dict()})

    # Swap the plates (swap the PlateInstance objects but keep their positions)
    plate_a = game.plates[from_index]
    plate_b = game.plates[to_index]

    # Swap positions
    pos_a = plate_a.position
    pos_b = plate_b.position
    plate_a.position = pos_b
    plate_b.position = pos_a

    # Swap in the list
    game.plates[from_index] = plate_b
    game.plates[to_index] = plate_a

    save_game(game)

    return jsonify({
        'success': True,
        'state': game.to_dict()
    })


@game_bp.route('/<game_id>', methods=['DELETE'])
def delete_game_endpoint(game_id):
    """Delete a game."""
    success = delete_game(game_id)
    if not success:
        return jsonify({'error': 'Game not found'}), 404

    return jsonify({'success': True})
