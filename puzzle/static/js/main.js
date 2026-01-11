/**
 * Main entry point for the puzzle game.
 */

import { api } from './api.js';
import { GameRenderer } from './renderer.js';
import { InteractionHandler } from './interactions.js';

class PuzzleGame {
    constructor() {
        this.gameId = null;
        this.gameState = null;
        this.pieceDefinitions = [];
        this.boardConfigurations = [];

        // DOM elements
        this.canvas = document.getElementById('game-canvas');
        this.boardSelector = document.getElementById('board-selector');
        this.pieceList = document.getElementById('piece-list');
        this.pieceCount = document.getElementById('piece-count');
        this.plateControls = document.getElementById('plate-controls');
        this.statusBar = document.getElementById('game-status');
        this.selectedPieceName = document.getElementById('selected-piece-name');
        this.victoryModal = document.getElementById('victory-modal');
        this.solvingOverlay = document.getElementById('solving-overlay');
        this.solvingStatus = document.getElementById('solving-status');
        this.solvingStats = document.getElementById('solving-stats');

        // Renderer and interaction handler
        this.renderer = new GameRenderer(this.canvas);
        this.interactions = new InteractionHandler(this.canvas, this.renderer, api, {
            onPieceSelected: (pieceId) => this.onPieceSelected(pieceId),
            onPiecePlaced: (result) => this.onPiecePlaced(result),
            onPieceRemoved: (result) => this.onPieceRemoved(result),
            onPuzzleSolved: () => this.onPuzzleSolved(),
            onError: (message) => this.setStatus(message, 'error'),
            onTransformChange: (rotation, flipped) => this.onTransformChange(rotation, flipped)
        });

        this.init();
    }

    async init() {
        try {
            // Load configurations and piece definitions
            const [configsResult, piecesResult] = await Promise.all([
                api.getConfigurations(),
                api.getPieces()
            ]);

            this.boardConfigurations = configsResult.configurations;
            this.pieceDefinitions = piecesResult.pieces;

            // Set up renderer with piece definitions
            this.renderer.setPieceDefinitions(this.pieceDefinitions);
            this.interactions.setPieceDefinitions(this.pieceDefinitions);

            // Populate UI
            this.populateBoardSelector();
            this.setupEventListeners();

            // Auto-start a game with the default board
            await this.newGame();
        } catch (error) {
            this.setStatus('Failed to initialize: ' + error.message, 'error');
        }
    }

    populateBoardSelector() {
        this.boardSelector.innerHTML = '';
        this.boardConfigurations.forEach(config => {
            const option = document.createElement('option');
            option.value = config.type;
            option.textContent = `${config.name} (${config.dimensions[0]}x${config.dimensions[1]})`;
            this.boardSelector.appendChild(option);
        });
    }

    setupEventListeners() {
        // Board selector - auto-create new game when changed
        this.boardSelector.addEventListener('change', () => this.newGame());

        // New game button
        document.getElementById('new-game').addEventListener('click', () => this.newGame());

        // Solve button
        document.getElementById('solve-btn').addEventListener('click', () => this.solve());

        // Hint button
        document.getElementById('hint-btn').addEventListener('click', () => this.getHint());

        // Reset button
        document.getElementById('reset-btn').addEventListener('click', () => this.reset());

        // Transform buttons
        document.getElementById('rotate-btn').addEventListener('click', () => {
            this.interactions.rotate();
        });
        document.getElementById('flip-btn').addEventListener('click', () => {
            this.interactions.flip();
        });
        document.getElementById('cancel-btn').addEventListener('click', () => {
            this.interactions.clearSelection();
        });

        // Victory modal
        document.getElementById('play-again-btn').addEventListener('click', () => {
            this.victoryModal.classList.add('hidden');
            this.newGame();
        });

        // Close modal button (view solution without starting new game)
        document.getElementById('close-modal-btn').addEventListener('click', () => {
            this.victoryModal.classList.add('hidden');
        });
    }

    async newGame() {
        const boardType = this.boardSelector.value;

        try {
            this.setStatus('Creating new game...');

            // Get plate configurations from UI (if game already exists)
            let plateConfigs = null;
            if (this.gameState) {
                plateConfigs = this.getPlateConfigsFromUI();
            }

            const result = await api.createGame(boardType, plateConfigs);

            this.gameId = result.game_id;
            this.gameState = result.state;

            this.interactions.setGameId(this.gameId);
            this.interactions.setGameState(this.gameState);
            this.renderer.setGameState(this.gameState);

            this.updateUI();
            this.renderer.render();

            this.setStatus('Game started! Select a piece to place.');
        } catch (error) {
            this.setStatus('Failed to create game: ' + error.message, 'error');
        }
    }

    getPlateConfigsFromUI() {
        const configs = [];
        for (let i = 0; i < 4; i++) {
            const sideSelect = document.getElementById(`plate-${i}-side`);
            const rotationSelect = document.getElementById(`plate-${i}-rotation`);

            if (sideSelect && rotationSelect) {
                configs.push({
                    plate_id: i + 1,
                    side: sideSelect.value,
                    rotation: parseInt(rotationSelect.value)
                });
            } else {
                configs.push({
                    plate_id: i + 1,
                    side: 'white',
                    rotation: 0
                });
            }
        }
        return configs;
    }

    updateUI() {
        this.updatePieceList();
        this.updatePlateControls();
        this.updatePieceCount();
    }

    updatePieceList() {
        this.pieceList.innerHTML = '';

        this.pieceDefinitions.forEach(piece => {
            const isAvailable = this.gameState?.available_pieces.includes(piece.id);

            const pieceEl = document.createElement('div');
            pieceEl.className = `piece-item ${isAvailable ? '' : 'placed'}`;
            pieceEl.dataset.pieceId = piece.id;

            // Mini canvas for piece preview
            const miniCanvas = document.createElement('canvas');
            miniCanvas.width = 60;
            miniCanvas.height = 60;
            this.renderer.drawPiecePreview(miniCanvas, piece);

            const label = document.createElement('span');
            label.textContent = piece.name;
            label.style.color = piece.color;

            pieceEl.appendChild(miniCanvas);
            pieceEl.appendChild(label);

            if (isAvailable) {
                pieceEl.addEventListener('click', () => {
                    this.selectPiece(piece.id);
                });
            }

            this.pieceList.appendChild(pieceEl);
        });
    }

    updatePlateControls() {
        if (!this.gameState) {
            this.plateControls.innerHTML = '<p>Start a game to configure plates</p>';
            return;
        }

        this.plateControls.innerHTML = '';

        this.gameState.plates.forEach((plate, index) => {
            const control = document.createElement('div');
            control.className = 'plate-control';
            control.draggable = true;
            control.dataset.plateIndex = index;

            control.innerHTML = `
                <div class="plate-drag-handle" title="Drag to swap with another plate">&#x2630;</div>
                <label>Plate ${plate.plate_id}:</label>
                <select id="plate-${index}-side">
                    <option value="white" ${plate.side === 'white' ? 'selected' : ''}>White</option>
                    <option value="black" ${plate.side === 'black' ? 'selected' : ''}>Black</option>
                </select>
                <select id="plate-${index}-rotation">
                    <option value="0" ${plate.rotation === 0 ? 'selected' : ''}>0°</option>
                    <option value="90" ${plate.rotation === 90 ? 'selected' : ''}>90°</option>
                    <option value="180" ${plate.rotation === 180 ? 'selected' : ''}>180°</option>
                    <option value="270" ${plate.rotation === 270 ? 'selected' : ''}>270°</option>
                </select>
            `;

            // Auto-apply when side or rotation changes
            const sideSelect = control.querySelector(`#plate-${index}-side`);
            const rotationSelect = control.querySelector(`#plate-${index}-rotation`);
            sideSelect.addEventListener('change', () => this.applyPlateConfig(index));
            rotationSelect.addEventListener('change', () => this.applyPlateConfig(index));

            // Drag and drop events
            control.addEventListener('dragstart', (e) => this.onPlateDragStart(e, index));
            control.addEventListener('dragend', (e) => this.onPlateDragEnd(e));
            control.addEventListener('dragover', (e) => this.onPlateDragOver(e));
            control.addEventListener('dragleave', (e) => this.onPlateDragLeave(e));
            control.addEventListener('drop', (e) => this.onPlateDrop(e, index));

            this.plateControls.appendChild(control);
        });
    }

    // Drag and drop handlers for plate swapping
    onPlateDragStart(e, index) {
        e.dataTransfer.setData('text/plain', index.toString());
        e.dataTransfer.effectAllowed = 'move';
        e.target.classList.add('dragging');
        this.draggedPlateIndex = index;
    }

    onPlateDragEnd(e) {
        e.target.classList.remove('dragging');
        // Remove drag-over class from all plate controls
        document.querySelectorAll('.plate-control').forEach(el => {
            el.classList.remove('drag-over');
        });
        this.draggedPlateIndex = null;
    }

    onPlateDragOver(e) {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
        const control = e.target.closest('.plate-control');
        if (control && parseInt(control.dataset.plateIndex) !== this.draggedPlateIndex) {
            control.classList.add('drag-over');
        }
    }

    onPlateDragLeave(e) {
        const control = e.target.closest('.plate-control');
        if (control) {
            control.classList.remove('drag-over');
        }
    }

    async onPlateDrop(e, toIndex) {
        e.preventDefault();
        const control = e.target.closest('.plate-control');
        if (control) {
            control.classList.remove('drag-over');
        }

        const fromIndex = parseInt(e.dataTransfer.getData('text/plain'));

        if (fromIndex === toIndex || isNaN(fromIndex)) {
            return;
        }

        await this.swapPlates(fromIndex, toIndex);
    }

    async swapPlates(fromIndex, toIndex) {
        if (!this.gameId) return;

        try {
            const result = await api.swapPlates(this.gameId, fromIndex, toIndex);

            if (result.success) {
                this.gameState = result.state;
                this.interactions.setGameState(this.gameState);
                this.renderer.setGameState(this.gameState);
                this.updatePlateControls();
                this.renderer.render();
                this.setStatus(`Swapped plate positions`);
            }
        } catch (error) {
            this.setStatus('Failed to swap plates: ' + error.message, 'error');
        }
    }

    async applyPlateConfig(plateIndex) {
        if (!this.gameId) return;

        const sideSelect = document.getElementById(`plate-${plateIndex}-side`);
        const rotationSelect = document.getElementById(`plate-${plateIndex}-rotation`);

        const currentPlate = this.gameState.plates[plateIndex];
        const newSide = sideSelect.value;
        const newRotation = parseInt(rotationSelect.value);

        try {
            // Check if side changed (need to flip)
            const needFlip = newSide !== currentPlate.side;

            const result = await api.rotatePlate(
                this.gameId,
                plateIndex,
                newRotation,
                needFlip
            );

            if (result.success) {
                this.gameState = result.state;
                this.interactions.setGameState(this.gameState);
                this.renderer.setGameState(this.gameState);
                this.renderer.render();
                this.setStatus('Plate configuration updated');
            }
        } catch (error) {
            this.setStatus('Failed to update plate: ' + error.message, 'error');
        }
    }

    updatePieceCount() {
        if (this.gameState) {
            this.pieceCount.textContent = this.gameState.available_pieces.length;
        } else {
            this.pieceCount.textContent = '12';
        }
    }

    selectPiece(pieceId) {
        // Update UI
        document.querySelectorAll('.piece-item').forEach(el => {
            el.classList.remove('selected');
        });
        const pieceEl = document.querySelector(`[data-piece-id="${pieceId}"]`);
        if (pieceEl) {
            pieceEl.classList.add('selected');
        }

        // Tell interaction handler
        this.interactions.selectPiece(pieceId);

        // Update status
        const piece = this.pieceDefinitions.find(p => p.id === pieceId);
        this.selectedPieceName.textContent = piece?.name || 'None';
        this.setStatus(`Selected ${piece?.name}. Click on the board to place.`);
    }

    onPieceSelected(pieceId) {
        if (pieceId) {
            const piece = this.pieceDefinitions.find(p => p.id === pieceId);
            this.selectedPieceName.textContent = piece?.name || 'None';
        } else {
            this.selectedPieceName.textContent = 'None';
            document.querySelectorAll('.piece-item').forEach(el => {
                el.classList.remove('selected');
            });
        }
    }

    onTransformChange(rotation, flipped) {
        // Could update UI to show current rotation/flip state
    }

    async onPiecePlaced(result) {
        this.gameState = result.state;
        this.interactions.setGameState(this.gameState);
        this.renderer.setGameState(this.gameState);
        this.updatePieceList();
        this.updatePieceCount();
        this.renderer.render();
        this.setStatus('Piece placed!', 'success');
    }

    async onPieceRemoved(result) {
        this.gameState = result.state;
        this.interactions.setGameState(this.gameState);
        this.renderer.setGameState(this.gameState);
        this.updatePieceList();
        this.updatePieceCount();
        this.renderer.render();
        this.setStatus('Piece removed');
    }

    onPuzzleSolved() {
        this.setStatus('Congratulations! Puzzle solved!', 'success');
        this.victoryModal.classList.remove('hidden');
    }

    async solve() {
        if (!this.gameId) {
            this.setStatus('Start a game first', 'error');
            return;
        }

        try {
            // Show solving overlay
            this.solvingOverlay.classList.remove('hidden');
            this.solvingStatus.textContent = 'Solving puzzle...';
            this.solvingStats.textContent = 'Searching for solution';

            // Get solution without applying it (we'll animate it)
            const result = await api.solve(this.gameId, 30, false);

            if (result.success && result.solution) {
                const stats = result.stats;
                this.solvingStatus.textContent = 'Solution found!';
                this.solvingStats.textContent = `${stats.time_elapsed_ms.toFixed(0)}ms, ${stats.nodes_explored} nodes explored`;

                // Wait a moment to show the "found" message
                await this.delay(500);

                // Hide overlay and animate placing pieces
                this.solvingOverlay.classList.add('hidden');
                await this.animateSolution(result.solution.placements);

                this.setStatus(
                    `Solved in ${stats.time_elapsed_ms.toFixed(0)}ms ` +
                    `(${stats.nodes_explored} nodes explored)`,
                    'success'
                );

                if (this.gameState.is_solved) {
                    // Delay showing victory modal so user can see the solution first
                    setTimeout(() => this.onPuzzleSolved(), 1000);
                }
            } else {
                this.solvingOverlay.classList.add('hidden');
                this.setStatus('No solution found: ' + result.message, 'error');
            }
        } catch (error) {
            this.solvingOverlay.classList.add('hidden');
            this.setStatus('Solve failed: ' + error.message, 'error');
        }
    }

    async animateSolution(placements) {
        // Place pieces one by one with animation delay
        for (let i = 0; i < placements.length; i++) {
            const placement = placements[i];

            this.setStatus(`Placing piece ${i + 1} of ${placements.length}: ${placement.piece_id.replace('_', ' ')}`);

            // Place the piece via API
            const result = await api.placePiece(
                this.gameId,
                placement.piece_id,
                placement.anchor_position,
                placement.rotation,
                placement.flipped
            );

            if (result.success) {
                this.gameState = result.state;
                this.interactions.setGameState(this.gameState);
                this.renderer.setGameState(this.gameState);
                this.updatePieceList();
                this.updatePieceCount();
                this.renderer.render();
            }

            // Delay between pieces (faster for more pieces)
            const delayMs = placements.length > 8 ? 150 : 250;
            await this.delay(delayMs);
        }
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async getHint() {
        if (!this.gameId) {
            this.setStatus('Start a game first', 'error');
            return;
        }

        try {
            const result = await api.getHint(this.gameId);

            if (result.success && result.hint) {
                const hint = result.hint;
                const piece = this.pieceDefinitions.find(p => p.id === hint.piece_id);

                // Select the piece with the suggested transform
                this.selectPiece(hint.piece_id);
                this.interactions.rotation = hint.rotation;
                this.interactions.flipped = hint.flipped;

                this.setStatus(
                    `Hint: Try ${piece?.name} at position (${hint.anchor_position[0]}, ${hint.anchor_position[1]})` +
                    ` with rotation ${hint.rotation}°${hint.flipped ? ' (flipped)' : ''}`
                );
            } else {
                this.setStatus(result.message || 'No hint available', 'error');
            }
        } catch (error) {
            this.setStatus('Hint failed: ' + error.message, 'error');
        }
    }

    async reset() {
        if (!this.gameId) {
            this.setStatus('Start a game first', 'error');
            return;
        }

        try {
            const result = await api.resetGame(this.gameId);

            if (result.success) {
                this.gameState = result.state;
                this.interactions.setGameState(this.gameState);
                this.interactions.clearSelection();
                this.renderer.setGameState(this.gameState);
                this.updateUI();
                this.renderer.render();
                this.setStatus('Game reset');
            }
        } catch (error) {
            this.setStatus('Reset failed: ' + error.message, 'error');
        }
    }

    setStatus(message, type = '') {
        this.statusBar.textContent = message;
        this.statusBar.className = type;
    }
}

// Initialize the game when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.puzzleGame = new PuzzleGame();
});
