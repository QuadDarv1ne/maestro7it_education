#!/usr/bin/env python3
"""
Enhanced Flask Web Server for Professional Chess Interface
Features:
- Modern responsive design
- Real-time game state
- WebSocket support for multiplayer
- Integration with C++ chess engine
- Enhanced UI/UX
"""

from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room
import json
import os
import sys
import threading
import time
from datetime import datetime
from collections import defaultdict

# Import chess engine components
# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from chess_engine_wrapper import chess_engine
    ENGINE_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Chess engine not available: {e}")
    ENGINE_AVAILABLE = False

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

# Game state management
games = {}
players = {}  # sid -> player_info
rooms = defaultdict(list)  # room_id -> [player_sids]

class EnhancedWebChess:
    """Enhanced chess game manager with real-time capabilities"""
    
    def __init__(self, game_id=None):
        self.game_id = game_id or str(time.time())
        self.board_state = self.get_initial_board()
        self.move_history = []
        self.current_player = 'white'
        self.game_active = True
        self.players = {'white': None, 'black': None}
        self.spectators = []
        self.created_at = datetime.now()
        self.last_move_time = None
        self.captured_pieces = {'white': [], 'black': []}
        
    def get_initial_board(self):
        """Return standard chess starting position"""
        return [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
    
    def reset_game(self):
        """Reset game to initial state"""
        self.board_state = self.get_initial_board()
        self.move_history = []
        self.current_player = 'white'
        self.game_active = True
        self.captured_pieces = {'white': [], 'black': []}
        self.last_move_time = None
    
    def make_move(self, from_pos, to_pos, player_sid=None):
        """Execute a move with validation"""
        if not self.game_active:
            return False, "Game is not active"
        
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Validate board boundaries
        if not all(0 <= x < 8 for x in [from_row, from_col, to_row, to_col]):
            return False, "Invalid coordinates"
        
        piece = self.board_state[from_row][from_col]
        if not piece:
            return False, "No piece at source position"
        
        # Validate player turn
        is_white_piece = piece.isupper()
        expected_player = 'white' if is_white_piece else 'black'
        
        if self.current_player != expected_player:
            return False, f"Not your turn. Current player: {self.current_player}"
        
        # Validate move legality (basic validation)
        if not self.is_valid_move(from_pos, to_pos):
            return False, "Invalid move"
        
        # Execute move
        captured_piece = self.board_state[to_row][to_col]
        
        # Record move
        move_record = {
            'from': from_pos,
            'to': to_pos,
            'piece': piece,
            'captured': captured_piece,
            'player': self.current_player,
            'timestamp': datetime.now().isoformat(),
            'player_sid': player_sid
        }
        
        self.move_history.append(move_record)
        
        # Update board
        self.board_state[to_row][to_col] = piece
        self.board_state[from_row][from_col] = None
        
        # Handle captured pieces
        if captured_piece:
            self.captured_pieces[self.current_player].append(captured_piece.upper())
        
        # Switch turns
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        self.last_move_time = datetime.now()
        
        return True, "Move executed successfully"
    
    def is_valid_move(self, from_pos, to_pos):
        """Basic move validation (simplified)"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = self.board_state[from_row][from_col]
        target_piece = self.board_state[to_row][to_col]
        
        # Cannot capture own piece
        if target_piece:
            if (piece.isupper() and target_piece.isupper()) or \
               (piece.islower() and target_piece.islower()):
                return False
        
        # Simplified piece movement rules
        piece_type = piece.lower()
        
        if piece_type == 'p':  # Pawn
            return self._validate_pawn_move(from_pos, to_pos, piece.isupper())
        elif piece_type == 'r':  # Rook
            return self._validate_rook_move(from_pos, to_pos)
        elif piece_type == 'n':  # Knight
            return self._validate_knight_move(from_pos, to_pos)
        elif piece_type == 'b':  # Bishop
            return self._validate_bishop_move(from_pos, to_pos)
        elif piece_type == 'q':  # Queen
            return self._validate_queen_move(from_pos, to_pos)
        elif piece_type == 'k':  # King
            return self._validate_king_move(from_pos, to_pos)
        
        return False
    
    def _validate_pawn_move(self, from_pos, to_pos, is_white):
        """Validate pawn movement"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        direction = -1 if is_white else 1
        start_row = 6 if is_white else 1
        
        # Forward move
        if from_col == to_col and to_row == from_row + direction and not self.board_state[to_row][to_col]:
            return True
        
        # Initial double move
        if (from_col == to_col and from_row == start_row and 
            to_row == from_row + 2 * direction and 
            not self.board_state[to_row][to_col] and 
            not self.board_state[from_row + direction][to_col]):
            return True
        
        # Diagonal capture
        if (abs(from_col - to_col) == 1 and to_row == from_row + direction and 
            self.board_state[to_row][to_col]):
            return True
        
        return False
    
    def _validate_rook_move(self, from_pos, to_pos):
        """Validate rook movement"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        if from_row != to_row and from_col != to_col:
            return False
        
        # Check path is clear
        if from_row == to_row:
            step = 1 if from_col < to_col else -1
            for col in range(from_col + step, to_col, step):
                if self.board_state[from_row][col]:
                    return False
        else:
            step = 1 if from_row < to_row else -1
            for row in range(from_row + step, to_row, step):
                if self.board_state[row][from_col]:
                    return False
        
        return True
    
    def _validate_knight_move(self, from_pos, to_pos):
        """Validate knight movement"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        row_diff = abs(from_row - to_row)
        col_diff = abs(from_col - to_col)
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)
    
    def _validate_bishop_move(self, from_pos, to_pos):
        """Validate bishop movement"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        if abs(from_row - to_row) != abs(from_col - to_col):
            return False
        
        row_step = 1 if to_row > from_row else -1
        col_step = 1 if to_col > from_col else -1
        
        row, col = from_row + row_step, from_col + col_step
        while row != to_row and col != to_col:
            if self.board_state[row][col]:
                return False
            row += row_step
            col += col_step
        
        return True
    
    def _validate_queen_move(self, from_pos, to_pos):
        """Validate queen movement"""
        return self._validate_rook_move(from_pos, to_pos) or self._validate_bishop_move(from_pos, to_pos)
    
    def _validate_king_move(self, from_pos, to_pos):
        """Validate king movement"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        return abs(from_row - to_row) <= 1 and abs(from_col - to_col) <= 1
    
    def get_game_state(self):
        """Get current game state for clients"""
        return {
            'board': self.board_state,
            'current_player': self.current_player,
            'move_history': self.move_history,
            'game_active': self.game_active,
            'captured_pieces': self.captured_pieces,
            'players': self.players,
            'created_at': self.created_at.isoformat(),
            'last_move_time': self.last_move_time.isoformat() if self.last_move_time else None
        }

# Routes
@app.route('/')
def index():
    """Serve the enhanced chess interface"""
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'enhanced_chess.html')

@app.route('/classic')
def classic_interface():
    """Serve the classic interface"""
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'index.html')

@app.route('/api/game-state/<game_id>')
def get_game_state(game_id):
    """Get current game state"""
    if game_id in games:
        return jsonify(games[game_id].get_game_state())
    return jsonify({'error': 'Game not found'}), 404

@app.route('/api/new-game', methods=['POST'])
def create_new_game():
    """Create a new game"""
    game = EnhancedWebChess()
    games[game.game_id] = game
    return jsonify({'game_id': game.game_id, 'status': 'created'})

# WebSocket events
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print(f"Client connected: {request.sid}")
    players[request.sid] = {
        'sid': request.sid,
        'username': f'Player_{request.sid[:8]}',
        'connected_at': datetime.now()
    }

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print(f"Client disconnected: {request.sid}")
    if request.sid in players:
        del players[request.sid]
    
    # Remove from rooms
    for room_id, player_list in list(rooms.items()):
        if request.sid in player_list:
            player_list.remove(request.sid)
            if not player_list:
                del rooms[room_id]
            socketio.emit('player_left', {'sid': request.sid}, room=room_id)

@socketio.on('join_game')
def handle_join_game(data):
    """Join a game room"""
    game_id = data.get('game_id')
    player_color = data.get('color', 'white')
    
    if not game_id or game_id not in games:
        emit('error', {'message': 'Game not found'})
        return
    
    game = games[game_id]
    
    # Check if color is available
    if game.players[player_color] is not None and game.players[player_color] != request.sid:
        emit('error', {'message': f'{player_color} player position already taken'})
        return
    
    # Join room
    join_room(game_id)
    game.players[player_color] = request.sid
    rooms[game_id].append(request.sid)
    
    # Notify others
    socketio.emit('player_joined', {
        'sid': request.sid,
        'color': player_color,
        'username': players[request.sid]['username']
    }, room=game_id)
    
    # Send current game state
    emit('game_state', game.get_game_state())

@socketio.on('make_move')
def handle_move(data):
    """Handle move request"""
    game_id = data.get('game_id')
    from_pos = data.get('from')
    to_pos = data.get('to')
    
    if not game_id or game_id not in games:
        emit('error', {'message': 'Game not found'})
        return
    
    game = games[game_id]
    
    # Verify player is authorized
    if request.sid not in [game.players['white'], game.players['black']]:
        emit('error', {'message': 'Not a player in this game'})
        return
    
    # Execute move
    success, message = game.make_move(from_pos, to_pos, request.sid)
    
    if success:
        # Broadcast move to all players in room
        socketio.emit('move_made', {
            'from': from_pos,
            'to': to_pos,
            'player': game.current_player,
            'game_state': game.get_game_state()
        }, room=game_id)
    else:
        emit('error', {'message': message})

@socketio.on('chat_message')
def handle_chat(data):
    """Handle chat messages"""
    game_id = data.get('game_id')
    message = data.get('message')
    
    if game_id and game_id in games:
        username = players.get(request.sid, {}).get('username', 'Unknown')
        socketio.emit('chat_message', {
            'username': username,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }, room=game_id)

@socketio.on('spectate_game')
def handle_spectate(data):
    """Join as spectator"""
    game_id = data.get('game_id')
    
    if game_id and game_id in games:
        join_room(game_id)
        games[game_id].spectators.append(request.sid)
        rooms[game_id].append(request.sid)
        emit('game_state', games[game_id].get_game_state())

if __name__ == '__main__':
    print("♔ ♕ ♖ ♗ ♘ ♙ ENHANCED CHESS SERVER STARTING ♟ ♞ ♝ ♜ ♛ ♚")
    print("=" * 50)
    print(f"Engine available: {ENGINE_AVAILABLE}")
    print("Available endpoints:")
    print("  / - Enhanced chess interface")
    print("  /classic - Classic interface")
    print("  /api/new-game - Create new game")
    print("  /api/game-state/<id> - Get game state")
    print("=" * 50)
    print("Starting server on http://localhost:5000")
    
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)