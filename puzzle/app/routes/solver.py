"""Solver API endpoints."""

from flask import Blueprint, request, jsonify

from app.models.game_state import get_game, save_game
from app.services.solver import PuzzleSolver

solver_bp = Blueprint('solver', __name__, url_prefix='/api/solver')


@solver_bp.route('/solve', methods=['POST'])
def solve():
    """
    Solve the current puzzle configuration.

    Request body:
    {
        "game_id": "abc123",
        "timeout": 30,  // optional, seconds
        "apply": false  // optional, apply solution to game state
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    game_id = data.get('game_id')
    if not game_id:
        return jsonify({'error': 'game_id is required'}), 400

    game = get_game(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404

    timeout = data.get('timeout', 30)
    apply_solution = data.get('apply', False)

    solver = PuzzleSolver(game, timeout_seconds=timeout)
    result = solver.solve()

    response = {
        'success': result.success,
        'message': result.message,
        'stats': {
            'nodes_explored': result.stats.nodes_explored,
            'solutions_found': result.stats.solutions_found,
            'time_elapsed_ms': result.stats.time_elapsed_ms,
            'pruned_branches': result.stats.pruned_branches
        }
    }

    if result.success and result.solution:
        response['solution'] = {
            'placements': [p.to_dict() for p in result.solution]
        }

        # Apply solution if requested
        if apply_solution:
            for placement in result.solution:
                game.place_piece(placement)
            save_game(game)
            response['state'] = game.to_dict()

    return jsonify(response)


@solver_bp.route('/hint', methods=['POST'])
def get_hint():
    """
    Get a hint for the next piece placement.

    Request body:
    {
        "game_id": "abc123"
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    game_id = data.get('game_id')
    if not game_id:
        return jsonify({'error': 'game_id is required'}), 400

    game = get_game(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404

    if game.is_solved():
        return jsonify({
            'success': True,
            'message': 'Puzzle already solved',
            'hint': None
        })

    solver = PuzzleSolver(game, timeout_seconds=5)
    hint = solver.get_hint()

    if hint:
        return jsonify({
            'success': True,
            'hint': hint.to_dict()
        })
    else:
        return jsonify({
            'success': False,
            'message': 'No valid placement found',
            'hint': None
        })


@solver_bp.route('/check-solvable', methods=['POST'])
def check_solvable():
    """
    Check if current configuration is solvable.

    Request body:
    {
        "game_id": "abc123"
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    game_id = data.get('game_id')
    if not game_id:
        return jsonify({'error': 'game_id is required'}), 400

    game = get_game(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404

    solver = PuzzleSolver(game, timeout_seconds=1)
    solvable, reason = solver.check_solvable()

    return jsonify({
        'solvable': solvable,
        'reason': reason
    })
