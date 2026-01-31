#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mobile Chess API - FastAPI Backend for Mobile Interface
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import json
import asyncio
from typing import List, Optional, Dict, Any
import sys
import os

# Add core to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))

try:
    from chess_engine_wrapper import ChessEngineWrapper
    from professional_endgame_tablebase import EndgameMaster
    from stockfish_nnue import EnhancedNeuralEvaluator
except ImportError as e:
    print(f"Warning: Some modules not available: {e}")
    ChessEngineWrapper = None
    EndgameMaster = None
    EnhancedNeuralEvaluator = None

app = FastAPI(title="Mobile Chess API", version="1.0.0")

# Serve static files
app.mount("/web", StaticFiles(directory="web"), name="web")

class MoveRequest(BaseModel):
    from_row: int
    from_col: int
    to_row: int
    to_col: int

class GameState(BaseModel):
    board: List[List[str]]
    current_player: str
    move_history: List[Dict]
    game_over: bool
    in_check: bool
    evaluation: float
    difficulty: int

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# Global game instances
game_engine = None
endgame_master = None
neural_evaluator = None

@app.on_event("startup")
async def startup_event():
    global game_engine, endgame_master, neural_evaluator
    
    print("🚀 Starting Mobile Chess API...")
    
    # Initialize chess engine components
    if ChessEngineWrapper:
        game_engine = ChessEngineWrapper()
        print("✅ Chess engine initialized")
    
    if EndgameMaster:
        endgame_master = EndgameMaster()
        print("✅ Endgame master initialized")
    
    if EnhancedNeuralEvaluator:
        neural_evaluator = EnhancedNeuralEvaluator()
        print("✅ Neural evaluator initialized")

@app.get("/", response_class=HTMLResponse)
async def get_mobile_interface():
    """Serve the mobile chess interface"""
    try:
        with open("web/mobile_chess.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Mobile interface not found</h1>", status_code=404)

@app.get("/api/game-state")
async def get_game_state() -> GameState:
    """Get current game state"""
    if not game_engine:
        return GameState(
            board=[['.' for _ in range(8)] for _ in range(8)],
            current_player="white",
            move_history=[],
            game_over=False,
            in_check=False,
            evaluation=0.0,
            difficulty=2
        )
    
    # Convert board to list format
    board_list = [list(row) for row in game_engine.board_state]
    
    # Calculate evaluation
    evaluation = 0.0
    if neural_evaluator:
        evaluation = neural_evaluator.evaluate_position(game_engine.board_state, game_engine.current_turn)
    elif hasattr(game_engine, 'evaluate_position'):
        evaluation = game_engine.evaluate_position()
    
    return GameState(
        board=board_list,
        current_player="white" if game_engine.current_turn else "black",
        move_history=getattr(game_engine, 'move_history', []),
        game_over=getattr(game_engine, 'game_over', False),
        in_check=getattr(game_engine, 'in_check', False),
        evaluation=float(evaluation),
        difficulty=getattr(game_engine, 'difficulty', 2)
    )

@app.post("/api/make-move")
async def make_move(move: MoveRequest):
    """Make a move on the board"""
    if not game_engine:
        return {"success": False, "error": "Game engine not initialized"}
    
    try:
        # Convert coordinates
        from_pos = (move.from_row, move.from_col)
        to_pos = (move.to_row, move.to_col)
        
        # Validate move
        is_valid = game_engine.is_valid_move_python(from_pos, to_pos)
        if not is_valid:
            return {"success": False, "error": "Invalid move"}
        
        # Make move
        success = game_engine.make_move(from_pos, to_pos)
        if not success:
            return {"success": False, "error": "Move failed"}
        
        # Check for game end
        game_status = check_game_status()
        
        # Get updated state
        state = await get_game_state()
        
        return {
            "success": True,
            "game_state": state,
            "game_status": game_status
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/new-game")
async def new_game():
    """Start a new game"""
    if not game_engine:
        return {"success": False, "error": "Game engine not initialized"}
    
    try:
        game_engine.__init__()  # Reset game
        state = await get_game_state()
        return {"success": True, "game_state": state}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/undo-move")
async def undo_move():
    """Undo the last move"""
    if not game_engine:
        return {"success": False, "error": "Game engine not initialized"}
    
    try:
        # This would need to be implemented in the engine
        if hasattr(game_engine, 'undo_move'):
            success = game_engine.undo_move()
            state = await get_game_state()
            return {"success": success, "game_state": state}
        else:
            return {"success": False, "error": "Undo not implemented"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/get-hint")
async def get_hint():
    """Get a hint for the best move"""
    if not game_engine:
        return {"success": False, "error": "Game engine not initialized"}
    
    try:
        # Get AI suggestion
        if hasattr(game_engine, 'get_best_move'):
            best_move = game_engine.get_best_move(depth=3)
            if best_move:
                return {
                    "success": True,
                    "hint": {
                        "from": [best_move[0][0], best_move[0][1]],
                        "to": [best_move[1][0], best_move[1][1]]
                    }
                }
        
        return {"success": False, "error": "Hint not available"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle WebSocket messages
            message = json.loads(data)
            
            if message["type"] == "move":
                # Handle move from WebSocket
                move_data = message["data"]
                # Process move and send update
                await manager.send_personal_message(json.dumps({"type": "move_confirmed"}), websocket)
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)

def check_game_status():
    """Check current game status"""
    if not game_engine:
        return "playing"
    
    # Check for checkmate, stalemate, etc.
    # This would need proper implementation in the engine
    return "playing"

@app.get("/api/stats")
async def get_engine_stats():
    """Get engine statistics"""
    stats = {
        "engine_status": "online" if game_engine else "offline",
        "endgame_status": "online" if endgame_master else "offline",
        "neural_status": "online" if neural_evaluator else "offline",
        "supported_features": []
    }
    
    if game_engine:
        stats["supported_features"].append("basic_moves")
        stats["supported_features"].append("validation")
    
    if endgame_master:
        stats["supported_features"].append("endgame_tablebase")
    
    if neural_evaluator:
        stats["supported_features"].append("neural_evaluation")
    
    return stats

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "components": {
            "game_engine": game_engine is not None,
            "endgame_master": endgame_master is not None,
            "neural_evaluator": neural_evaluator is not None
        }
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Mobile Chess Server...")
    print("📱 Access mobile interface at: http://localhost:8000")
    print("🔌 API documentation at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")