"""Flask application factory."""

from flask import Flask
from flask_cors import CORS


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__,
                static_folder='../static',
                template_folder='../templates')

    # Enable CORS for API endpoints
    CORS(app)

    # Register blueprints
    from app.routes.game import game_bp
    from app.routes.solver import solver_bp
    from app.routes.board import board_bp

    app.register_blueprint(game_bp)
    app.register_blueprint(solver_bp)
    app.register_blueprint(board_bp)

    # Main route to serve the game
    @app.route('/')
    def index():
        from flask import render_template
        return render_template('index.html')

    return app
