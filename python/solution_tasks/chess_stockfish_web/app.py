# app.py
from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit, disconnect
from stockfish import Stockfish
import os
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'maestro7it-chess-secret'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store game instances per session
games = {}

class ChessGame:
    def __init__(self, player_color='white', skill_level=5):
        self.player_color = player_color
        self.skill_level = skill_level
        self.engine = None
        self.initialized = False
        self.init_engine()
    
    def init_engine(self):
        try:
            # Check for local stockfish executable first
            local_stockfish_path = os.path.join(os.path.dirname(__file__), 'stockfish.exe')
            if os.path.exists(local_stockfish_path):
                self.engine = Stockfish(path=local_stockfish_path)
            else:
                # Check for STOCKFISH_PATH environment variable
                path = os.getenv('STOCKFISH_PATH', None)
                if path and os.path.exists(path):
                    self.engine = Stockfish(path=path)
                else:
                    # Try to use stockfish from PATH
                    self.engine = Stockfish()
            
            self.engine.set_skill_level(self.skill_level)
            self.engine.set_depth(15)  # Increased depth for better moves
            self.initialized = True
            return True
        except Exception as e:
            print(f"Stockfish initialization error: {e}")
            return False
    
    def get_fen(self):
        if self.engine:
            return self.engine.get_fen_position()
        return None
    
    def make_move(self, move):
        if not self.initialized or not self.engine:
            return False
        # make_moves_from_current_position returns None on success, False on failure
        result = self.engine.make_moves_from_current_position([move])
        return result is not False
    
    def is_move_correct(self, move):
        """
        Check if a move is correct.
        Note: The stockfish library's is_move_correct method seems to have issues,
        so we'll use a more reliable approach by checking if the move actually changes the position.
        """
        if not self.initialized or not self.engine:
            return False
            
        # Save current position
        fen_before = self.engine.get_fen_position()
        
        # Try to make the move
        result = self.engine.make_moves_from_current_position([move])
        
        # Check if position changed
        fen_after = self.engine.get_fen_position()
        move_successful = (result is not False) and (fen_before != fen_after)
        
        # If move was successful, undo it to maintain current state
        if move_successful:
            # Reset to previous position
            self.engine.set_fen_position(fen_before)
        
        return move_successful
    
    def get_best_move(self):
        if not self.initialized or not self.engine:
            return None
        return self.engine.get_best_move()

@app.route('/')
def index():
    # Generate a unique session ID for each user
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    # Create a session ID for Socket.IO connection if it doesn't exist
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())

@socketio.on('disconnect')
def handle_disconnect():
    session_id = session.get('session_id')
    if session_id and session_id in games:
        # Clean up game instance when user disconnects
        del games[session_id]

@socketio.on('init_game')
def handle_init(data):
    session_id = session.get('session_id')
    
    if not session_id:
        emit('error', {'message': 'Session error'})
        return
    
    try:
        player_color = data.get('color', 'white')
        skill_level = min(20, max(0, int(data.get('level', 5))))
        
        # Create a new game instance for this session
        game = ChessGame(player_color, skill_level)
        
        if game.initialized:
            games[session_id] = game
            fen = game.get_fen()
            emit('game_initialized', {'fen': fen, 'player_color': player_color})
        else:
            emit('error', {'message': 'Failed to start Stockfish engine'})
    except Exception as e:
        emit('error', {'message': 'Game initialization error'})

@socketio.on('make_move')
def handle_move(data):
    try:
        session_id = session.get('session_id')
        if not session_id or session_id not in games:
            emit('error', {'message': 'Game not initialized'})
            return

        game = games[session_id]
        uci_move = data['move']

        # Validate move format
        if not isinstance(uci_move, str) or len(uci_move) != 4:
            emit('invalid_move', {'move': uci_move, 'message': 'Invalid move format'})
            return

        if game.is_move_correct(uci_move):
            if not game.make_move(uci_move):
                emit('invalid_move', {'move': uci_move, 'message': 'Invalid move'})
                return
                
            fen = game.get_fen()

            # Check game status
            if ' w ' in fen:
                # Check for checkmate or stalemate for white
                if '#' in fen and not any(c.isupper() for c in fen.split()[0] if c.isalpha()):
                    emit('game_over', {'result': 'checkmate', 'fen': fen, 'winner': 'black'})
                    return
            else:
                # Check for checkmate or stalemate for black
                if '#' in fen and not any(c.islower() for c in fen.split()[0] if c.isalpha()):
                    emit('game_over', {'result': 'checkmate', 'fen': fen, 'winner': 'white'})
                    return
            
            # Check for stalemate (simplified)
            if not game.engine.get_best_move():
                emit('game_over', {'result': 'stalemate', 'fen': fen})
                return

            # AI move
            ai_move = game.get_best_move()
            if ai_move:
                if not game.make_move(ai_move):
                    emit('position_update', {'fen': fen})
                    return
                    
                fen = game.get_fen()
                
                # Check game status after AI move
                if ' w ' in fen:
                    if '#' in fen and not any(c.isupper() for c in fen.split()[0] if c.isalpha()):
                        emit('game_over', {'result': 'checkmate', 'fen': fen, 'winner': 'black'})
                        return
                else:
                    if '#' in fen and not any(c.islower() for c in fen.split()[0] if c.isalpha()):
                        emit('game_over', {'result': 'checkmate', 'fen': fen, 'winner': 'white'})
                        return
                
                # Check for stalemate after AI move
                if not game.engine.get_best_move():
                    emit('game_over', {'result': 'stalemate', 'fen': fen})
                    return
                    
                emit('position_update', {'fen': fen, 'ai_move': ai_move})
            else:
                emit('position_update', {'fen': fen})
        else:
            emit('invalid_move', {'move': uci_move, 'message': 'Invalid move'})
    except Exception as e:
        emit('error', {'message': 'Move processing error'})

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5001, debug=False)