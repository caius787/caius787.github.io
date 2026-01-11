/**
 * API service for communicating with the backend.
 */

const API_BASE = '/api';

export const api = {
    /**
     * Get all available board configurations.
     */
    async getConfigurations() {
        const response = await fetch(`${API_BASE}/board/configurations`);
        return response.json();
    },

    /**
     * Get details of a specific board configuration.
     */
    async getConfiguration(boardType) {
        const response = await fetch(`${API_BASE}/board/configurations/${boardType}`);
        return response.json();
    },

    /**
     * Get all piece definitions.
     */
    async getPieces() {
        const response = await fetch(`${API_BASE}/board/pieces`);
        return response.json();
    },

    /**
     * Get all plate definitions.
     */
    async getPlates() {
        const response = await fetch(`${API_BASE}/board/plates`);
        return response.json();
    },

    /**
     * Create a new game.
     */
    async createGame(boardType, plateConfigs = null) {
        const body = { board_type: boardType };
        if (plateConfigs) {
            body.plates = plateConfigs;
        }
        const response = await fetch(`${API_BASE}/game/new`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
        return response.json();
    },

    /**
     * Get current game state.
     */
    async getGameState(gameId) {
        const response = await fetch(`${API_BASE}/game/${gameId}/state`);
        return response.json();
    },

    /**
     * Place a piece on the board.
     */
    async placePiece(gameId, pieceId, position, rotation = 0, flipped = false) {
        const response = await fetch(`${API_BASE}/game/${gameId}/place`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                piece_id: pieceId,
                position: position,
                rotation: rotation,
                flipped: flipped
            })
        });
        return response.json();
    },

    /**
     * Remove a placed piece.
     */
    async removePiece(gameId, pieceId) {
        const response = await fetch(`${API_BASE}/game/${gameId}/remove`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ piece_id: pieceId })
        });
        return response.json();
    },

    /**
     * Validate a piece placement.
     */
    async validatePlacement(gameId, pieceId, position, rotation = 0, flipped = false) {
        const response = await fetch(`${API_BASE}/game/${gameId}/validate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                piece_id: pieceId,
                position: position,
                rotation: rotation,
                flipped: flipped
            })
        });
        return response.json();
    },

    /**
     * Reset the game.
     */
    async resetGame(gameId) {
        const response = await fetch(`${API_BASE}/game/${gameId}/reset`, {
            method: 'POST'
        });
        return response.json();
    },

    /**
     * Rotate or flip a plate.
     */
    async rotatePlate(gameId, plateIndex, rotation = null, flip = false) {
        const body = { plate_index: plateIndex };
        if (rotation !== null) body.rotation = rotation;
        if (flip) body.flip = true;

        const response = await fetch(`${API_BASE}/game/${gameId}/rotate-plate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
        return response.json();
    },

    /**
     * Swap two plates in the layout.
     */
    async swapPlates(gameId, fromIndex, toIndex) {
        const response = await fetch(`${API_BASE}/game/${gameId}/swap-plates`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                from_index: fromIndex,
                to_index: toIndex
            })
        });
        return response.json();
    },

    /**
     * Auto-solve the puzzle.
     */
    async solve(gameId, timeout = 30, apply = false) {
        const response = await fetch(`${API_BASE}/solver/solve`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                game_id: gameId,
                timeout: timeout,
                apply: apply
            })
        });
        return response.json();
    },

    /**
     * Get a hint for the next piece.
     */
    async getHint(gameId) {
        const response = await fetch(`${API_BASE}/solver/hint`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ game_id: gameId })
        });
        return response.json();
    },

    /**
     * Check if puzzle is solvable.
     */
    async checkSolvable(gameId) {
        const response = await fetch(`${API_BASE}/solver/check-solvable`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ game_id: gameId })
        });
        return response.json();
    }
};
