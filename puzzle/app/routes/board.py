"""Board configuration API endpoints."""

from flask import Blueprint, jsonify

from app.models.board import BoardType, BoardBuilder
from app.models.piece import PIECE_DEFINITIONS
from app.models.plate import PLATE_DEFINITIONS, slot_to_coords

board_bp = Blueprint('board', __name__, url_prefix='/api/board')


@board_bp.route('/configurations', methods=['GET'])
def list_configurations():
    """
    List all available board configurations.
    """
    configurations = []

    for board_type in BoardType:
        config = BoardBuilder.build(board_type)
        configurations.append({
            'type': board_type.value,
            'name': board_type.name.replace('_', ' ').title(),
            'description': config.description,
            'dimensions': [config.total_height, config.total_width]
        })

    return jsonify({'configurations': configurations})


@board_bp.route('/configurations/<board_type>', methods=['GET'])
def get_configuration(board_type):
    """
    Get details of a specific board configuration.
    """
    # Convert string to BoardType enum
    try:
        bt = BoardType(board_type)
    except ValueError:
        try:
            bt = BoardType[board_type.upper()]
        except KeyError:
            return jsonify({
                'error': f'Invalid board type: {board_type}',
                'valid_types': [b.value for b in BoardType]
            }), 404

    config = BoardBuilder.build(bt)
    return jsonify(config.to_dict())


@board_bp.route('/pieces', methods=['GET'])
def list_pieces():
    """
    List all piece definitions.
    """
    pieces = []

    for piece_id, piece_def in PIECE_DEFINITIONS.items():
        pieces.append(piece_def.to_dict())

    return jsonify({'pieces': pieces})


@board_bp.route('/pieces/<piece_id>', methods=['GET'])
def get_piece(piece_id):
    """
    Get details of a specific piece.
    """
    piece_def = PIECE_DEFINITIONS.get(piece_id)
    if not piece_def:
        return jsonify({
            'error': f'Invalid piece: {piece_id}',
            'valid_pieces': list(PIECE_DEFINITIONS.keys())
        }), 404

    return jsonify(piece_def.to_dict())


@board_bp.route('/plates', methods=['GET'])
def list_plates():
    """
    List all plate definitions.
    """
    plates = []

    for plate_id, plate_def in PLATE_DEFINITIONS.items():
        plates.append({
            'plate_id': plate_id,
            'white_obstructions': list(plate_def.white_obstructions),
            'black_obstructions': list(plate_def.black_obstructions),
            'white_obstruction_coords': [
                list(slot_to_coords(s)) for s in plate_def.white_obstructions
            ],
            'black_obstruction_coords': [
                list(slot_to_coords(s)) for s in plate_def.black_obstructions
            ]
        })

    return jsonify({'plates': plates})
