#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FastAPI Chess Web Application
Modern, high-performance chess web interface with real-time capabilities
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
from core.chess_engine_wrapper import ChessEngineWrapper
from core.optimized_move_generator import BitboardMoveGenerator
from core.enhanced_chess_ai import EnhancedChessAI

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
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main chess application page"""
    try:
        with open("web/fastapi_index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Chess Web UI not found</h1><p>Please ensure web/fastapi_index.html exists.</p>"

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
        from_pos = tuple(request.from_pos)
        to_pos = tuple(request.to_pos)
        
        # Execute move using engine
        success = engine.make_move(from_pos, to_pos)
        
        if success:
            # Record move for web UI
            move_record = {
                'from': from_pos,
                'to': to_pos,
                'piece': engine.board_state[to_pos[0]][to_pos[1]],
                'notation': engine.move_history[-1] if engine.move_history else "",
                'timestamp': datetime.now().isoformat()
            }
            game['move_history'].append(move_record)
            
            return {
                'success': True,
                'game_state': GameResponse(
                    game_id=request.game_id,
                    board_state=engine.board_state,
                    current_turn=engine.current_turn,
                    game_status="active",
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

@app.get("/api/valid-moves/{game_id}")
async def get_valid_moves(game_id: str, r: int, c: int):
    """Get valid moves for a piece at (r, c)"""
    game = game_manager.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    engine = game['engine']
    moves = []
    for tr in range(8):
        for tc in range(8):
            if engine.is_valid_move((r, c), (tr, tc)):
                moves.append([tr, tc])
    return {"moves": moves}

@app.get("/api/evaluation/{game_id}")
async def get_evaluation(game_id: str):
    """Get position evaluation"""
    game = game_manager.get_game(game_id)
    if not game:
        return {"evaluation": 0}
    
    return {"evaluation": game['engine'].get_evaluation()}

@app.get("/api/ai-move/{game_id}")
async def get_ai_move(game_id: str, depth: int = 4):
    """Get AI move for the current position"""
    try:
        game = game_manager.get_game(game_id)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        
        engine = game['engine']
        best_move = engine.get_best_move(depth=depth)
        
        if best_move:
            from_pos, to_pos = best_move
            engine.make_move(from_pos, to_pos)
            
            # Record move
            move_record = {
                'from': from_pos,
                'to': to_pos,
                'piece': engine.board_state[to_pos[0]][to_pos[1]],
                'notation': engine.move_history[-1] if engine.move_history else "",
                'timestamp': datetime.now().isoformat()
            }
            game['move_history'].append(move_record)
            
            return {
                'success': True,
                'move_notation': move_record['notation'],
                'ai_stats': engine.get_game_statistics(),
                'game_state': GameResponse(
                    game_id=game_id,
                    board_state=engine.board_state,
                    current_turn=engine.current_turn,
                    game_status="active",
                    move_history=game['move_history'],
                    player_name=game['player_name'],
                    game_mode=game['game_mode']
                )
            }
        return {"success": False, "message": "No moves available"}
    except Exception as e:
        logger.error(f"AI Move Error: {e}")
        return {"success": False, "message": str(e)}

@app.post("/api/save-game/{game_id}")
async def save_game(game_id: str):
    """Save the current game state to a file"""
    game = game_manager.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    success = game['engine'].save_game("web_chess_save.json")
    return {"success": success}

@app.post("/api/load-game")
async def load_game():
    """Load game state from file"""
    # For now, we load into a new game session
    game_id = game_manager.create_game("Loaded Player", "ai")
    game = game_manager.get_game(game_id)
    
    success = game['engine'].load_game("web_chess_save.json")
    if success:
        # Update move history from engine if needed
        game['move_history'] = [] # Need to reconstruct if necessary, or engine handles it
        return {
            "success": True, 
            "game_id": game_id,
            "game_state": GameResponse(
                game_id=game_id,
                board_state=game['engine'].board_state,
                current_turn=game['engine'].current_turn,
                game_status="active",
                move_history=[],
                player_name=game['player_name'],
                game_mode=game['game_mode']
            )
        }
    return {"success": False}

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