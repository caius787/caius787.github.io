/**
 * Interaction handler for the puzzle game.
 */

export class InteractionHandler {
    constructor(canvas, renderer, api, callbacks) {
        this.canvas = canvas;
        this.renderer = renderer;
        this.api = api;
        this.callbacks = callbacks;

        this.gameId = null;
        this.gameState = null;
        this.pieceDefinitions = {};

        this.selectedPiece = null;
        this.rotation = 0;
        this.flipped = false;

        this.setupEventListeners();
    }

    setGameId(gameId) {
        this.gameId = gameId;
    }

    setGameState(gameState) {
        this.gameState = gameState;
    }

    setPieceDefinitions(pieces) {
        this.pieceDefinitions = {};
        pieces.forEach(p => {
            this.pieceDefinitions[p.id] = p;
        });
    }

    setupEventListeners() {
        this.canvas.addEventListener('mousemove', this.handleMouseMove.bind(this));
        this.canvas.addEventListener('click', this.handleClick.bind(this));
        this.canvas.addEventListener('contextmenu', this.handleRightClick.bind(this));
        this.canvas.addEventListener('mouseleave', this.handleMouseLeave.bind(this));

        // Keyboard shortcuts
        document.addEventListener('keydown', this.handleKeyDown.bind(this));
    }

    handleMouseMove(event) {
        if (!this.selectedPiece || !this.gameState) return;

        const rect = this.canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        const [row, col] = this.renderer.canvasToBoard(x, y);

        // Calculate piece coordinates
        const coords = this.calculateOccupiedCoords(row, col);

        // Check validity
        const valid = this.checkPlacementValid(coords);

        // Update hover preview
        this.renderer.setHoverPreview({
            pieceId: this.selectedPiece,
            coords: coords
        }, valid);

        this.renderer.render();
    }

    async handleClick(event) {
        if (!this.gameId || !this.gameState) return;

        const rect = this.canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        const [row, col] = this.renderer.canvasToBoard(x, y);

        // If no piece selected, check if clicking on a placed piece to remove it
        if (!this.selectedPiece) {
            const clickedPiece = this.findPieceAtPosition(row, col);
            if (clickedPiece) {
                await this.removePiece(clickedPiece);
            }
            return;
        }

        // Try to place the piece
        await this.placePiece(row, col);
    }

    handleRightClick(event) {
        event.preventDefault();
        if (this.selectedPiece) {
            this.rotate();
        }
    }

    handleMouseLeave() {
        this.renderer.clearHoverPreview();
        this.renderer.render();
    }

    handleKeyDown(event) {
        switch (event.key.toLowerCase()) {
            case 'r':
                this.rotate();
                break;
            case 'f':
                this.flip();
                break;
            case 'escape':
                this.clearSelection();
                break;
        }
    }

    rotate() {
        this.rotation = (this.rotation + 90) % 360;
        this.updatePreview();
        this.callbacks.onTransformChange?.(this.rotation, this.flipped);
    }

    flip() {
        this.flipped = !this.flipped;
        this.updatePreview();
        this.callbacks.onTransformChange?.(this.rotation, this.flipped);
    }

    updatePreview() {
        // Trigger a fake mouse move to update the preview
        const rect = this.canvas.getBoundingClientRect();
        const event = new MouseEvent('mousemove', {
            clientX: rect.left + this.canvas.width / 2,
            clientY: rect.top + this.canvas.height / 2
        });
        this.handleMouseMove(event);
    }

    selectPiece(pieceId) {
        this.selectedPiece = pieceId;
        this.rotation = 0;
        this.flipped = false;
        this.canvas.style.cursor = 'crosshair';
        this.callbacks.onPieceSelected?.(pieceId);
    }

    clearSelection() {
        this.selectedPiece = null;
        this.rotation = 0;
        this.flipped = false;
        this.renderer.clearHoverPreview();
        this.renderer.render();
        this.canvas.style.cursor = 'default';
        this.callbacks.onPieceSelected?.(null);
    }

    async placePiece(row, col) {
        if (!this.selectedPiece || !this.gameId) return;

        const coords = this.calculateOccupiedCoords(row, col);
        if (!this.checkPlacementValid(coords)) {
            this.callbacks.onError?.('Invalid placement');
            return;
        }

        try {
            const result = await this.api.placePiece(
                this.gameId,
                this.selectedPiece,
                [row, col],
                this.rotation,
                this.flipped
            );

            if (result.success) {
                this.clearSelection();
                this.callbacks.onPiecePlaced?.(result);

                if (result.is_solved) {
                    this.callbacks.onPuzzleSolved?.();
                }
            } else {
                this.callbacks.onError?.('Failed to place piece');
            }
        } catch (error) {
            this.callbacks.onError?.(error.message);
        }
    }

    async removePiece(pieceId) {
        if (!this.gameId) return;

        try {
            const result = await this.api.removePiece(this.gameId, pieceId);
            if (result.success) {
                this.callbacks.onPieceRemoved?.(result);
            }
        } catch (error) {
            this.callbacks.onError?.(error.message);
        }
    }

    findPieceAtPosition(row, col) {
        if (!this.gameState) return null;

        for (const [pieceId, placement] of Object.entries(this.gameState.placed_pieces)) {
            const coords = placement.occupied_coords;
            if (coords.some(([r, c]) => r === row && c === col)) {
                return pieceId;
            }
        }
        return null;
    }

    calculateOccupiedCoords(anchorRow, anchorCol) {
        const pieceDef = this.pieceDefinitions[this.selectedPiece];
        if (!pieceDef) return [];

        // Get base shape and transform it
        let coords = pieceDef.shape.map(c => [...c]);

        // Apply flip
        if (this.flipped) {
            coords = coords.map(([r, c]) => [r, -c]);
        }

        // Apply rotation
        for (let i = 0; i < this.rotation / 90; i++) {
            coords = coords.map(([r, c]) => [c, -r]);
        }

        // Normalize
        if (coords.length > 0) {
            const minRow = Math.min(...coords.map(c => c[0]));
            const minCol = Math.min(...coords.map(c => c[1]));
            coords = coords.map(([r, c]) => [r - minRow, c - minCol]);
        }

        // Offset by anchor
        return coords.map(([r, c]) => [r + anchorRow, c + anchorCol]);
    }

    checkPlacementValid(coords) {
        if (!this.gameState) return false;

        const validCells = new Set(
            this.gameState.board_config.valid_cells.map(c => `${c[0]},${c[1]}`)
        );
        const obstructedCells = new Set(
            this.gameState.obstructed_cells.map(c => `${c[0]},${c[1]}`)
        );
        const occupiedCells = new Set(
            this.gameState.occupied_cells.map(c => `${c[0]},${c[1]}`)
        );

        for (const [row, col] of coords) {
            const key = `${row},${col}`;

            // Check bounds
            if (!validCells.has(key)) return false;

            // Check obstructions
            if (obstructedCells.has(key)) return false;

            // Check collisions
            if (occupiedCells.has(key)) return false;
        }

        return true;
    }
}
