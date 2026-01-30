#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FastAPI Chess Web Application
Modern, high-performance chess web interface with real-time capabilities
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional, Tuple
import asyncio
import json
import uuid
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import chess components
from chess_engine_wrapper import ChessEngineWrapper
from optimized_move_generator import BitboardMoveGenerator
from enhanced_chess_ai import EnhancedChessAI

app = FastAPI(
    title="Chess Engine API",
    description="High-performance chess engine with FastAPI backend",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="web"), name="static")

# Game management
class GameManager:
    def __init__(self):
        self.games: Dict[str, dict] = {}
        self.connections: Dict[str, List[WebSocket]] = {}
    
    def create_game(self, player_name: str = "Anonymous", game_mode: str = "ai") -> str:
        game_id = str(uuid.uuid4())
        self.games[game_id] = {
            'id': game_id,
            'player_name': player_name,
            'game_mode': game_mode,
            'engine': ChessEngineWrapper(),
            'ai': EnhancedChessAI(search_depth=4) if game_mode == "ai" else None,
            'move_generator': BitboardMoveGenerator(),
            'created_at': datetime.now(),
            'last_move_time': datetime.now(),
            'move_history': [],
            'current_player': True,  # True = white, False = black
            'game_status': 'active',  # active, check, checkmate, stalemate
            'winner': None
        }
        self.connections[game_id] = []
        logger.info(f"Created game {game_id} for player {player_name}")
        return game_id
    
    def get_game(self, game_id: str) -> Optional[dict]:
        return self.games.get(game_id)
    
    def delete_game(self, game_id: str):
        if game_id in self.games:
            del self.games[game_id]
        if game_id in self.connections:
            del self.connections[game_id]
        logger.info(f"Deleted game {game_id}")

game_manager = GameManager()

# Pydantic models
class MoveRequest(BaseModel):
    game_id: str
    from_pos: Tuple[int, int]
    to_pos: Tuple[int, int]
    player_color: bool  # True = white, False = black

class GameRequest(BaseModel):
    player_name: str = "Anonymous"
    game_mode: str = "ai"  # "ai" or "human"
    player_color: bool = True  # True = white, False = black

class GameResponse(BaseModel):
    game_id: str
    board_state: List[List[str]]
    current_turn: bool
    game_status: str
    move_history: List[Dict]
    player_name: str
    game_mode: str

# HTML templates
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chess Engine - FastAPI</title>
    <style>
        :root {
            --primary-color: #2c3e50;
            --secondary-color: #3498db;
            --accent-color: #e74c3c;
            --light-bg: #ecf0f1;
            --dark-bg: #34495e;
            --text-light: #ffffff;
            --text-dark: #2c3e50;
            --success: #27ae60;
            --warning: #f39c12;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--dark-bg) 100%);
            color: var(--text-light);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        
        header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            background: linear-gradient(45deg, var(--secondary-color), var(--accent-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .game-info {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            flex-wrap: wrap;
            gap: 15px;
        }
        
        .info-card {
            background: rgba(255, 255, 255, 0.15);
            padding: 15px 20px;
            border-radius: 10px;
            min-width: 150px;
        }
        
        .info-card h3 {
            font-size: 0.9rem;
            opacity: 0.8;
            margin-bottom: 5px;
        }
        
        .info-card p {
            font-size: 1.2rem;
            font-weight: bold;
        }
        
        .chess-board {
            display: grid;
            grid-template-columns: repeat(8, 1fr);
            grid-template-rows: repeat(8, 1fr);
            width: 500px;
            height: 500px;
            margin: 0 auto 30px;
            border: 3px solid var(--secondary-color);
            border-radius: 8px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        }
        
        .square {
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2.5rem;
            cursor: pointer;
            transition: all 0.2s ease;
            position: relative;
        }
        
        .square.light {
            background-color: #f0d9b5;
        }
        
        .square.dark {
            background-color: #b58863;
        }
        
        .square.selected {
            background-color: rgba(52, 152, 219, 0.7);
            box-shadow: inset 0 0 15px rgba(0, 0, 0, 0.3);
        }
        
        .square.valid-move {
            background-color: rgba(46, 204, 113, 0.5);
        }
        
        .square:hover:not(.empty):not(.selected) {
            transform: scale(1.05);
            z-index: 10;
        }
        
        .controls {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-top: 20px;
            flex-wrap: wrap;
        }
        
        button {
            padding: 12px 25px;
            font-size: 1rem;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            background: var(--secondary-color);
            color: white;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        }
        
        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        #newGameBtn {
            background: var(--success);
        }
        
        #undoBtn {
            background: var(--warning);
        }
        
        .status-bar {
            text-align: center;
            padding: 15px;
            margin: 20px 0;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 8px;
            font-size: 1.1rem;
            font-weight: bold;
        }
        
        .move-history {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
            max-height: 200px;
            overflow-y: auto;
        }
        
        .move-history h3 {
            margin-bottom: 15px;
            color: var(--secondary-color);
        }
        
        .move-list {
            display: grid;
            grid-template-columns: 50px 1fr 1fr;
            gap: 10px;
            font-family: monospace;
        }
        
        .move-number {
            font-weight: bold;
            color: var(--accent-color);
        }
        
        @media (max-width: 768px) {
            .chess-board {
                width: 90vw;
                height: 90vw;
                max-width: 400px;
                max-height: 400px;
            }
            
            .square {
                font-size: 1.8rem;
            }
            
            h1 {
                font-size: 2rem;
            }
            
            .game-info {
                flex-direction: column;
                align-items: stretch;
            }
        }
        
        /* Animations */
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        .pulse {
            animation: pulse 0.5s ease-in-out;
        }
        
        .highlight-check {
            animation: pulse 2s infinite;
            box-shadow: 0 0 20px var(--warning);
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>♔ Modern Chess Engine ♛</h1>
            <p>Powered by FastAPI & Advanced Algorithms</p>
        </header>
        
        <div class="game-info">
            <div class="info-card">
                <h3>Game ID</h3>
                <p id="gameId">-</p>
            </div>
            <div class="info-card">
                <h3>Status</h3>
                <p id="gameStatus">Ready</p>
            </div>
            <div class="info-card">
                <h3>Turn</h3>
                <p id="currentTurn">White</p>
            </div>
            <div class="info-card">
                <h3>Moves</h3>
                <p id="moveCount">0</p>
            </div>
        </div>
        
        <div class="status-bar" id="statusBar">
            Welcome! Select a piece to start playing.
        </div>
        
        <div class="chess-board" id="chessBoard"></div>
        
        <div class="controls">
            <button id="newGameBtn" onclick="newGame()">New Game</button>
            <button id="undoBtn" onclick="undoMove()" disabled>Undo Move</button>
            <button onclick="showHistory()">Move History</button>
        </div>
        
        <div class="move-history" id="moveHistory" style="display: none;">
            <h3>Move History</h3>
            <div class="move-list" id="moveList"></div>
        </div>
    </div>

    <script>
        // Global variables
        let gameId = null;
        let currentPlayerColor = true; // true = white
        let selectedSquare = null;
        let validMoves = [];
        let websocket = null;
        let gameState = null;
        
        // Unicode chess pieces
        const pieces = {
            'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
            'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
        };
        
        // Initialize the game
        document.addEventListener('DOMContentLoaded', async function() {
            await newGame();
            connectWebSocket();
        });
        
        async function newGame() {
            try {
                const response = await fetch('/api/new-game', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        player_name: 'Player',
                        game_mode: 'ai',
                        player_color: true
                    })
                });
                
                const data = await response.json();
                if (data.game_id) {
                    gameId = data.game_id;
                    gameState = data;
                    updateGameInfo(data);
                    renderBoard(data.board_state);
                    document.getElementById('undoBtn').disabled = data.move_history.length === 0;
                }
            } catch (error) {
                console.error('Error creating new game:', error);
                showStatus('Failed to create new game', 'error');
            }
        }
        
        function connectWebSocket() {
            if (websocket) {
                websocket.close();
            }
            
            const wsUrl = `ws://${window.location.host}/ws/${gameId}`;
            websocket = new WebSocket(wsUrl);
            
            websocket.onopen = function(event) {
                console.log('WebSocket connected');
            };
            
            websocket.onmessage = function(event) {
                const data = JSON.parse(event.data);
                if (data.type === 'game_update') {
                    gameState = data.game_state;
                    updateGameInfo(gameState);
                    renderBoard(gameState.board_state);
                    document.getElementById('undoBtn').disabled = gameState.move_history.length === 0;
                } else if (data.type === 'move_made') {
                    showStatus(`Move made: ${data.move_notation}`, 'success');
                }
            };
            
            websocket.onerror = function(error) {
                console.error('WebSocket error:', error);
            };
            
            websocket.onclose = function(event) {
                console.log('WebSocket closed');
            };
        }
        
        function renderBoard(board) {
            const boardElement = document.getElementById('chessBoard');
            boardElement.innerHTML = '';
            
            for (let row = 0; row < 8; row++) {
                for (let col = 0; col < 8; col++) {
                    const square = document.createElement('div');
                    square.className = `square ${(row + col) % 2 === 0 ? 'light' : 'dark'}`;
                    square.dataset.row = row;
                    square.dataset.col = col;
                    
                    const piece = board[row][col];
                    if (piece !== '.') {
                        square.textContent = pieces[piece];
                        square.classList.add(piece === piece.toUpperCase() ? 'white-piece' : 'black-piece');
                    } else {
                        square.classList.add('empty');
                    }
                    
                    square.addEventListener('click', () => handleSquareClick(row, col));
                    boardElement.appendChild(square);
                }
            }
        }
        
        function handleSquareClick(row, col) {
            const board = gameState.board_state;
            const piece = board[row][col];
            
            // Clear previous selections
            clearSelections();
            
            // If clicking on own piece
            if (piece !== '.' && 
                ((currentPlayerColor && piece === piece.toUpperCase()) ||
                 (!currentPlayerColor && piece === piece.toLowerCase()))) {
                
                selectedSquare = [row, col];
                document.querySelector(`[data-row="${row}"][data-col="${col}"]`).classList.add('selected');
                
                // Highlight valid moves
                highlightValidMoves(row, col);
            }
            // If clicking on valid move square
            else if (selectedSquare && validMoves.some(move => move[0] === row && move[1] === col)) {
                makeMove(selectedSquare[0], selectedSquare[1], row, col);
            }
        }
        
        async function makeMove(fromRow, fromCol, toRow, toCol) {
            try {
                const response = await fetch('/api/make-move', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        game_id: gameId,
                        from_pos: [fromRow, fromCol],
                        to_pos: [toRow, toCol],
                        player_color: currentPlayerColor
                    })
                });
                
                const data = await response.json();
                if (data.success) {
                    gameState = data.game_state;
                    updateGameInfo(gameState);
                    renderBoard(gameState.board_state);
                    clearSelections();
                    document.getElementById('undoBtn').disabled = false;
                    
                    // If playing against AI, let AI make its move
                    if (gameState.game_mode === 'ai' && gameState.current_turn !== currentPlayerColor) {
                        setTimeout(makeAIMove, 500);
                    }
                } else {
                    showStatus(data.message || 'Invalid move', 'error');
                }
            } catch (error) {
                console.error('Error making move:', error);
                showStatus('Failed to make move', 'error');
            }
        }
        
        async function makeAIMove() {
            try {
                const response = await fetch(`/api/ai-move/${gameId}`);
                const data = await response.json();
                
                if (data.success) {
                    gameState = data.game_state;
                    updateGameInfo(gameState);
                    renderBoard(gameState.board_state);
                    showStatus(`AI moved: ${data.move_notation}`, 'info');
                }
            } catch (error) {
                console.error('Error getting AI move:', error);
            }
        }
        
        function highlightValidMoves(row, col) {
            // In a real implementation, this would call the backend to get valid moves
            // For now, we'll simulate some basic moves
            validMoves = [];
            
            // Simple pawn moves (this is a simplified version)
            if (currentPlayerColor) { // White pawn
                if (row > 0 && gameState.board_state[row-1][col] === '.') {
                    validMoves.push([row-1, col]);
                }
            } else { // Black pawn
                if (row < 7 && gameState.board_state[row+1][col] === '.') {
                    validMoves.push([row+1, col]);
                }
            }
            
            // Highlight valid moves
            validMoves.forEach(([r, c]) => {
                document.querySelector(`[data-row="${r}"][data-col="${c}"]`).classList.add('valid-move');
            });
        }
        
        function clearSelections() {
            document.querySelectorAll('.square').forEach(square => {
                square.classList.remove('selected', 'valid-move');
            });
            selectedSquare = null;
            validMoves = [];
        }
        
        function updateGameInfo(state) {
            document.getElementById('gameId').textContent = state.game_id.substring(0, 8) + '...';
            document.getElementById('gameStatus').textContent = state.game_status;
            document.getElementById('currentTurn').textContent = state.current_turn ? 'White' : 'Black';
            document.getElementById('moveCount').textContent = state.move_history.length;
        }
        
        function showStatus(message, type = 'info') {
            const statusBar = document.getElementById('statusBar');
            statusBar.textContent = message;
            statusBar.className = `status-bar ${type}`;
            
            // Remove status after 3 seconds
            setTimeout(() => {
                statusBar.textContent = 'Game in progress...';
                statusBar.className = 'status-bar';
            }, 3000);
        }
        
        function showHistory() {
            const historyDiv = document.getElementById('moveHistory');
            const moveList = document.getElementById('moveList');
            
            if (historyDiv.style.display === 'none') {
                historyDiv.style.display = 'block';
                moveList.innerHTML = '';
                
                gameState.move_history.forEach((move, index) => {
                    const moveDiv = document.createElement('div');
                    moveDiv.className = 'move-item';
                    moveDiv.innerHTML = `
                        <span class="move-number">${Math.floor(index/2) + 1}${index % 2 === 0 ? '.' : '...'}</span>
                        <span>${move.notation || move.from + '-' + move.to}</span>
                        <span>${move.timestamp || ''}</span>
                    `;
                    moveList.appendChild(moveDiv);
                });
            } else {
                historyDiv.style.display = 'none';
            }
        }
        
        async function undoMove() {
            try {
                const response = await fetch(`/api/undo-move/${gameId}`, {
                    method: 'POST'
                });
                
                const data = await response.json();
                if (data.success) {
                    gameState = data.game_state;
                    updateGameInfo(gameState);
                    renderBoard(gameState.board_state);
                    document.getElementById('undoBtn').disabled = gameState.move_history.length === 0;
                    showStatus('Move undone', 'success');
                }
            } catch (error) {
                console.error('Error undoing move:', error);
                showStatus('Cannot undo move', 'error');
            }
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main chess application page"""
    return HTML_TEMPLATE

@app.post("/api/new-game")
async def create_new_game(request: GameRequest):
    """Create a new chess game"""
    try:
        game_id = game_manager.create_game(request.player_name, request.game_mode)
        game = game_manager.get_game(game_id)
        
        return GameResponse(
            game_id=game_id,
            board_state=game['engine'].board_state,
            current_turn=game['engine'].current_turn,
            game_status=game['game_status'],
            move_history=game['move_history'],
            player_name=request.player_name,
            game_mode=request.game_mode
        )
    except Exception as e:
        logger.error(f"Error creating game: {e}")
        raise HTTPException(status_code=500, detail="Failed to create game")

@app.post("/api/make-move")
async def make_move(request: MoveRequest):
    """Make a move in the chess game"""
    try:
        game = game_manager.get_game(request.game_id)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        
        engine = game['engine']
        from_pos = request.from_pos
        to_pos = request.to_pos
        
        # Validate move
        if engine.is_valid_move(from_pos, to_pos):
            # Execute move
            piece = engine.board_state[from_pos[0]][from_pos[1]]
            target = engine.board_state[to_pos[0]][to_pos[1]]
            
            engine.board_state[to_pos[0]][to_pos[1]] = piece
            engine.board_state[from_pos[0]][from_pos[1]] = '.'
            engine.current_turn = not engine.current_turn
            
            # Record move
            move_record = {
                'from': from_pos,
                'to': to_pos,
                'piece': piece,
                'captured': target if target != '.' else None,
                'timestamp': datetime.now().isoformat()
            }
            game['move_history'].append(move_record)
            game['last_move_time'] = datetime.now()
            
            # Check game status
            game_status = check_game_status(engine.board_state, engine.current_turn)
            game['game_status'] = game_status
            
            return {
                'success': True,
                'game_state': GameResponse(
                    game_id=request.game_id,
                    board_state=engine.board_state,
                    current_turn=engine.current_turn,
                    game_status=game_status,
                    move_history=game['move_history'],
                    player_name=game['player_name'],
                    game_mode=game['game_mode']
                )
            }
        else:
            return {
                'success': False,
                'message': 'Invalid move'
            }
            
    except Exception as e:
        logger.error(f"Error making move: {e}")
        raise HTTPException(status_code=500, detail="Failed to make move")

@app.get("/api/ai-move/{game_id}")
async def get_ai_move(game_id: str):
    """Get AI move for the current position"""
    try:
        game = game_manager.get_game(game_id)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        
        if not game['ai']:
            raise HTTPException(status_code=400, detail="No AI in this game")
        
        # Get AI move
        ai_move = game['ai'].get_best_move(game['engine'].board_state, game['engine'].current_turn)
        
        if ai_move:
            from_pos, to_pos = ai_move
            # Execute AI move
            engine = game['engine']
            piece = engine.board_state[from_pos[0]][from_pos[1]]
            target = engine.board_state[to_pos[0]][to_pos[1]]
            
            engine.board_state[to_pos[0]][to_pos[1]] = piece
            engine.board_state[from_pos[0]][from_pos[1]] = '.'
            engine.current_turn = not engine.current_turn
            
            # Record move
            move_record = {
                'from': from_pos,
                'to': to_pos,
                'piece': piece,
                'captured': target if target != '.' else None,
                'timestamp': datetime.now().isoformat()
            }
            game['move_history'].append(move_record)
            
            # Convert to algebraic notation
            move_notation = convert_to_algebraic(from_pos, to_pos, piece)
            
            return {
                'success': True,
                'move_notation': move_notation,
                'game_state': GameResponse(
                    game_id=game_id,
                    board_state=engine.board_state,
                    current_turn=engine.current_turn,
                    game_status=game['game_status'],
                    move_history=game['move_history'],
                    player_name=game['player_name'],
                    game_mode=game['game_mode']
                )
            }
        else:
            raise HTTPException(status_code=500, detail="AI could not generate move")
            
    except Exception as e:
        logger.error(f"Error getting AI move: {e}")
        raise HTTPException(status_code=500, detail="Failed to get AI move")

@app.post("/api/undo-move/{game_id}")
async def undo_move(game_id: str):
    """Undo the last move"""
    try:
        game = game_manager.get_game(game_id)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        
        if not game['move_history']:
            raise HTTPException(status_code=400, detail="No moves to undo")
        
        # Get last move
        last_move = game['move_history'].pop()
        
        # Restore board state
        engine = game['engine']
        engine.board_state[last_move['from'][0]][last_move['from'][1]] = last_move['piece']
        engine.board_state[last_move['to'][0]][last_move['to'][1]] = last_move['captured'] or '.'
        engine.current_turn = not engine.current_turn
        
        return {
            'success': True,
            'game_state': GameResponse(
                game_id=game_id,
                board_state=engine.board_state,
                current_turn=engine.current_turn,
                game_status=game['game_status'],
                move_history=game['move_history'],
                player_name=game['player_name'],
                game_mode=game['game_mode']
            )
        }
        
    except Exception as e:
        logger.error(f"Error undoing move: {e}")
        raise HTTPException(status_code=500, detail="Failed to undo move")

def check_game_status(board: List[List[str]], current_turn: bool) -> str:
    """Check current game status"""
    # This is a simplified implementation
    # In a full implementation, you'd check for check, checkmate, stalemate
    return "active"

def convert_to_algebraic(from_pos: Tuple[int, int], to_pos: Tuple[int, int], piece: str) -> str:
    """Convert move coordinates to algebraic notation"""
    files = 'abcdefgh'
    ranks = '87654321'
    
    from_square = files[from_pos[1]] + ranks[from_pos[0]]
    to_square = files[to_pos[1]] + ranks[to_pos[0]]
    
    piece_symbol = piece.upper() if piece.isupper() else piece.lower()
    return f"{piece_symbol}{from_square}-{to_square}"

# WebSocket endpoint for real-time updates
@app.websocket("/ws/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str):
    """WebSocket endpoint for real-time game updates"""
    await websocket.accept()
    
    try:
        # Add connection to game
        if game_id in game_manager.connections:
            game_manager.connections[game_id].append(websocket)
        
        while True:
            # Keep connection alive
            await asyncio.sleep(1)
            
    except WebSocketDisconnect:
        # Remove connection
        if game_id in game_manager.connections:
            if websocket in game_manager.connections[game_id]:
                game_manager.connections[game_id].remove(websocket)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")