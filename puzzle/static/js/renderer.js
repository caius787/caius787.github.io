/**
 * Canvas renderer for the puzzle game.
 */

export class GameRenderer {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.cellSize = 40;
        this.padding = 20;
        this.gameState = null;
        this.pieceDefinitions = {};
        this.hoverPreview = null;
        this.hoverValid = true;

        // Colors
        this.colors = {
            background: '#222',
            plateWhite: '#f5f5f5',
            plateBlack: '#333',
            obstruction: '#e94560',
            gridLine: '#444',
            gridLinePlate: '#666',
            validCell: '#1a3a1a',
            hoverValid: 'rgba(76, 175, 80, 0.5)',
            hoverInvalid: 'rgba(244, 67, 54, 0.5)',
            placed: '#2a2a4a'
        };
    }

    setGameState(gameState) {
        this.gameState = gameState;
        this.resizeCanvas();
    }

    setPieceDefinitions(pieces) {
        this.pieceDefinitions = {};
        pieces.forEach(p => {
            this.pieceDefinitions[p.id] = p;
        });
    }

    setHoverPreview(preview, valid = true) {
        this.hoverPreview = preview;
        this.hoverValid = valid;
    }

    clearHoverPreview() {
        this.hoverPreview = null;
    }

    resizeCanvas() {
        if (!this.gameState) return;

        const config = this.gameState.board_config;
        const width = config.dimensions[1] * this.cellSize + this.padding * 2;
        const height = config.dimensions[0] * this.cellSize + this.padding * 2;

        this.canvas.width = width;
        this.canvas.height = height;
    }

    render() {
        if (!this.gameState) return;

        this.clear();
        this.drawValidCells();
        this.drawPlates();
        this.drawObstructions();
        this.drawPlacedPieces();
        this.drawHoverPreview();
        this.drawGridLines();
    }

    clear() {
        this.ctx.fillStyle = this.colors.background;
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    }

    drawValidCells() {
        if (!this.gameState) return;

        const validCells = new Set(
            this.gameState.board_config.valid_cells.map(c => `${c[0]},${c[1]}`)
        );

        this.ctx.fillStyle = this.colors.validCell;

        for (const cellKey of validCells) {
            const [row, col] = cellKey.split(',').map(Number);
            const x = this.padding + col * this.cellSize;
            const y = this.padding + row * this.cellSize;
            this.ctx.fillRect(x, y, this.cellSize, this.cellSize);
        }
    }

    drawPlates() {
        if (!this.gameState) return;

        this.gameState.plates.forEach((plate, index) => {
            const pos = plate.position;
            const x = this.padding + pos[1] * this.cellSize;
            const y = this.padding + pos[0] * this.cellSize;
            const size = 4 * this.cellSize;

            // Plate background with subtle color difference
            this.ctx.fillStyle = plate.side === 'white'
                ? 'rgba(255, 255, 255, 0.05)'
                : 'rgba(0, 0, 0, 0.1)';
            this.ctx.fillRect(x, y, size, size);

            // Plate border
            this.ctx.strokeStyle = plate.side === 'white' ? '#555' : '#333';
            this.ctx.lineWidth = 2;
            this.ctx.strokeRect(x, y, size, size);

            // Plate label
            this.ctx.fillStyle = '#666';
            this.ctx.font = '10px sans-serif';
            this.ctx.fillText(`P${plate.plate_id}`, x + 4, y + 12);
        });
    }

    drawObstructions() {
        if (!this.gameState) return;

        const obstructedCells = this.gameState.obstructed_cells;

        obstructedCells.forEach(([row, col]) => {
            const x = this.padding + col * this.cellSize;
            const y = this.padding + row * this.cellSize;

            // Draw obstruction background
            this.ctx.fillStyle = this.colors.obstruction;
            this.ctx.fillRect(x + 2, y + 2, this.cellSize - 4, this.cellSize - 4);

            // Draw X pattern
            this.ctx.strokeStyle = '#fff';
            this.ctx.lineWidth = 2;
            this.ctx.beginPath();
            this.ctx.moveTo(x + 8, y + 8);
            this.ctx.lineTo(x + this.cellSize - 8, y + this.cellSize - 8);
            this.ctx.moveTo(x + this.cellSize - 8, y + 8);
            this.ctx.lineTo(x + 8, y + this.cellSize - 8);
            this.ctx.stroke();
        });
    }

    drawPlacedPieces() {
        if (!this.gameState) return;

        Object.entries(this.gameState.placed_pieces).forEach(([pieceId, placement]) => {
            const pieceDef = this.pieceDefinitions[pieceId];
            if (!pieceDef) return;

            const coords = placement.occupied_coords;
            this.drawPieceCells(coords, pieceDef.color, false);
        });
    }

    drawHoverPreview() {
        if (!this.hoverPreview) return;

        const { pieceId, coords } = this.hoverPreview;
        const pieceDef = this.pieceDefinitions[pieceId];
        if (!pieceDef) return;

        const color = this.hoverValid ? this.colors.hoverValid : this.colors.hoverInvalid;
        this.drawPieceCells(coords, color, true);

        // Also draw piece outline with actual color
        if (this.hoverValid) {
            coords.forEach(([row, col]) => {
                const x = this.padding + col * this.cellSize;
                const y = this.padding + row * this.cellSize;
                this.ctx.strokeStyle = pieceDef.color;
                this.ctx.lineWidth = 2;
                this.ctx.strokeRect(x + 2, y + 2, this.cellSize - 4, this.cellSize - 4);
            });
        }
    }

    drawPieceCells(coords, color, isPreview = false) {
        coords.forEach(([row, col]) => {
            const x = this.padding + col * this.cellSize;
            const y = this.padding + row * this.cellSize;

            // Fill
            this.ctx.fillStyle = color;
            this.ctx.fillRect(x + 1, y + 1, this.cellSize - 2, this.cellSize - 2);

            if (!isPreview) {
                // Add slight 3D effect for placed pieces
                this.ctx.fillStyle = 'rgba(255, 255, 255, 0.2)';
                this.ctx.fillRect(x + 1, y + 1, this.cellSize - 2, 4);
                this.ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
                this.ctx.fillRect(x + 1, y + this.cellSize - 5, this.cellSize - 2, 4);
            }
        });

        // Draw ball/dimple effect for non-preview pieces
        if (!isPreview) {
            coords.forEach(([row, col]) => {
                const x = this.padding + col * this.cellSize + this.cellSize / 2;
                const y = this.padding + row * this.cellSize + this.cellSize / 2;
                const radius = this.cellSize / 3;

                // Gradient for 3D ball effect
                const gradient = this.ctx.createRadialGradient(
                    x - radius / 3, y - radius / 3, 0,
                    x, y, radius
                );
                gradient.addColorStop(0, 'rgba(255, 255, 255, 0.4)');
                gradient.addColorStop(1, 'rgba(0, 0, 0, 0.2)');

                this.ctx.beginPath();
                this.ctx.arc(x, y, radius, 0, Math.PI * 2);
                this.ctx.fillStyle = gradient;
                this.ctx.fill();
            });
        }
    }

    drawGridLines() {
        if (!this.gameState) return;

        const config = this.gameState.board_config;
        const width = config.dimensions[1];
        const height = config.dimensions[0];

        this.ctx.strokeStyle = this.colors.gridLine;
        this.ctx.lineWidth = 0.5;

        // Vertical lines
        for (let col = 0; col <= width; col++) {
            const x = this.padding + col * this.cellSize;
            this.ctx.beginPath();
            this.ctx.moveTo(x, this.padding);
            this.ctx.lineTo(x, this.padding + height * this.cellSize);
            this.ctx.stroke();
        }

        // Horizontal lines
        for (let row = 0; row <= height; row++) {
            const y = this.padding + row * this.cellSize;
            this.ctx.beginPath();
            this.ctx.moveTo(this.padding, y);
            this.ctx.lineTo(this.padding + width * this.cellSize, y);
            this.ctx.stroke();
        }
    }

    // Coordinate conversion
    canvasToBoard(canvasX, canvasY) {
        const col = Math.floor((canvasX - this.padding) / this.cellSize);
        const row = Math.floor((canvasY - this.padding) / this.cellSize);
        return [row, col];
    }

    boardToCanvas(row, col) {
        return [
            this.padding + col * this.cellSize,
            this.padding + row * this.cellSize
        ];
    }

    // Draw a piece preview in a small canvas (for piece tray)
    drawPiecePreview(canvas, piece) {
        const ctx = canvas.getContext('2d');
        const cellSize = 12;
        const padding = 4;

        // Clear
        ctx.fillStyle = 'transparent';
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Get piece shape
        const shape = piece.shape;
        if (!shape || shape.length === 0) return;

        // Find bounds
        const maxRow = Math.max(...shape.map(c => c[0]));
        const maxCol = Math.max(...shape.map(c => c[1]));

        // Center the piece
        const offsetX = (canvas.width - (maxCol + 1) * cellSize) / 2;
        const offsetY = (canvas.height - (maxRow + 1) * cellSize) / 2;

        // Draw cells
        shape.forEach(([row, col]) => {
            const x = offsetX + col * cellSize;
            const y = offsetY + row * cellSize;

            ctx.fillStyle = piece.color;
            ctx.fillRect(x + 1, y + 1, cellSize - 2, cellSize - 2);

            // Simple highlight
            ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
            ctx.fillRect(x + 1, y + 1, cellSize - 2, 2);
        });
    }
}
