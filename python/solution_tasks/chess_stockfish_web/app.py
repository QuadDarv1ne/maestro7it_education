# app.py
from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit, disconnect
from stockfish import Stockfish
import os
import uuid
import sys
import time
import logging
import json
import threading
import weakref

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def cleanup_stale_games():
    """Periodically clean up stale game sessions to prevent memory leaks."""
    global games, session_timestamps, active_game_count
    while True:
        try:
            time.sleep(CLEANUP_INTERVAL)
            current_time = time.time()
            
            # Find stale sessions
            stale_sessions = [
                session_id for session_id, timestamp in session_timestamps.items()
                if current_time - timestamp > GAME_TIMEOUT
            ]
            
            # Clean up stale sessions
            for session_id in stale_sessions:
                if session_id in games:
                    # Clean up game resources
                    try:
                        del games[session_id]
                        active_game_count = max(0, active_game_count - 1)
                        logger.info(f"Cleaned up stale game for session: {session_id}")
                    except Exception as e:
                        logger.error(f"Error cleaning up stale game for session {session_id}: {e}")
                
                # Remove timestamp
                if session_id in session_timestamps:
                    del session_timestamps[session_id]
            
            logger.info(f"Cleanup completed. Active games: {active_game_count}, Tracked sessions: {len(session_timestamps)}")
        except Exception as e:
            logger.error(f"Error in cleanup thread: {e}")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'maestro7it-chess-secret'
socketio = SocketIO(app, cors_allowed_origins="*", ping_timeout=30, ping_interval=25)

# Start cleanup thread
cleanup_thread = threading.Thread(target=cleanup_stale_games, daemon=True)
cleanup_thread.start()

# Store game instances per session
games = {}

# Global Stockfish engine instance for reuse
stockfish_engine = None

# Maximum concurrent games to prevent server overload
MAX_CONCURRENT_GAMES = 10

# Track active game count
active_game_count = 0

# Session timestamps for cleanup
session_timestamps = {}

# Cleanup interval in seconds
CLEANUP_INTERVAL = 300  # 5 minutes

# Game inactivity timeout in seconds
GAME_TIMEOUT = 3600  # 1 hour

class ChessGame:
    def __init__(self, player_color='white', skill_level=5):
        self.player_color = player_color
        self.skill_level = skill_level
        self.engine = None
        self.initialized = False
        # Don't initialize engine here, do it lazily when needed
        
    def _is_engine_compatible(self, engine, skill_level):
        """
        Check if the existing engine can be reused with the requested skill level.
        For simplicity, we'll assume compatibility and just update the skill level.
        """
        try:
            engine.set_skill_level(skill_level)
            return True
        except:
            return False
    
    def init_engine(self):
        global stockfish_engine
        start_time = time.time()
        try:
            # Reuse existing engine if available and properly configured
            if stockfish_engine and self._is_engine_compatible(stockfish_engine, self.skill_level):
                logger.info(f"Reusing existing Stockfish engine with skill level {self.skill_level}")
                self.engine = stockfish_engine
                # Configure engine for optimal performance
                self.engine.set_depth(10)  # Reduced depth for faster moves, adjustable
                self.engine.update_engine_parameters({
                    'Threads': 2,  # Use multiple threads for better performance
                    'Hash': 128,   # Allocate 128 MB hash for position evaluation
                    'Contempt': 0, # Neutral contempt factor
                    'Ponder': False # Disable pondering for faster response
                })
                self.initialized = True
                logger.info(f"Engine reuse took {time.time() - start_time:.2f} seconds")
                return True
            
            # Initialize new engine
            # Check for local stockfish executable first
            local_stockfish_path = os.path.join(os.path.dirname(__file__), 'stockfish.exe')
            if os.path.exists(local_stockfish_path):
                logger.info(f"Using local Stockfish executable: {local_stockfish_path}")
                self.engine = Stockfish(path=local_stockfish_path)
            else:
                # Check for STOCKFISH_PATH environment variable
                path = os.getenv('STOCKFISH_PATH', None)
                if path and os.path.exists(path):
                    logger.info(f"Using Stockfish from STOCKFISH_PATH: {path}")
                    self.engine = Stockfish(path=path)
                else:
                    # Try to use stockfish from PATH
                    logger.info("Using Stockfish from system PATH")
                    self.engine = Stockfish()
            
            # Configure engine for optimal performance
            self.engine.set_skill_level(self.skill_level)
            self.engine.set_depth(10)  # Reduced depth for faster moves, adjustable
            self.engine.update_engine_parameters({
                'Threads': 2,  # Use multiple threads for better performance
                'Hash': 128,   # Allocate 128 MB hash for position evaluation
                'Contempt': 0, # Neutral contempt factor
                'Ponder': False # Disable pondering for faster response
            })
            
            # Store engine for reuse
            stockfish_engine = self.engine
            self.initialized = True
            logger.info(f"Stockfish engine initialized successfully with skill level {self.skill_level} in {time.time() - start_time:.2f} seconds")
            return True
        except Exception as e:
            logger.error(f"Stockfish initialization error: {e}")
            import traceback
            traceback.print_exc()
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
        Check if a move is correct using Stockfish's built-in validation for better performance.
        If that fails, fall back to position comparison method.
        """
        if not self.initialized or not self.engine:
            return False
            
        # First try using Stockfish's built-in validation (faster)
        try:
            return self.engine.is_move_correct(move)
        except:
            # Fall back to position comparison method if built-in validation fails
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
    
    def get_game_status(self, fen):
        """
        Determine the game status (check, checkmate, stalemate) from the FEN string.
        Returns a dictionary with game status information.
        """
        if not fen:
            return {'game_over': False}
        
        # Check for checkmate using Stockfish evaluation
        if self.engine:
            try:
                # Get evaluation to check for checkmate
                evaluation = self.engine.get_evaluation()
                if evaluation and 'type' in evaluation:
                    if evaluation['type'] == 'mate' and evaluation['value'] == 0:
                        # Mate in 0 means current player is checkmated
                        winner = 'black' if 'w' in fen else 'white'
                        return {
                            'game_over': True,
                            'result': 'checkmate',
                            'winner': winner
                        }
                    elif evaluation['type'] == 'cp' and evaluation['value'] == 0:
                        # Check for stalemate by seeing if any legal moves exist
                        if not self.engine.get_best_move():
                            return {
                                'game_over': True,
                                'result': 'stalemate'
                            }
            except:
                # Fallback to FEN-based detection if evaluation fails
                pass
        
        # Fallback to original FEN-based detection
        if '#' in fen:
            # Check for checkmate
            if ' w ' in fen:
                # White to move, but in checkmate
                if not any(c.isupper() for c in fen.split()[0] if c.isalpha()):
                    return {
                        'game_over': True,
                        'result': 'checkmate',
                        'winner': 'black'
                    }
            else:
                # Black to move, but in checkmate
                if not any(c.islower() for c in fen.split()[0] if c.isalpha()):
                    return {
                        'game_over': True,
                        'result': 'checkmate',
                        'winner': 'white'
                    }
        
        return {'game_over': False}

@app.route('/')
def index():
    # Generate a unique session ID for each user
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    print(f"DEBUG: HTTP session created with session_id: {session.get('session_id')}")
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    try:
        # Create a session ID for Socket.IO connection if it doesn't exist
        logger.info("WebSocket connect event received")
        logger.info(f"Current session keys: {list(session.keys())}")
        logger.info(f"Current session_id: {session.get('session_id')}")
        
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
            logger.info(f"Created new session_id for WebSocket: {session.get('session_id')}")
        else:
            logger.info(f"Using existing session_id for WebSocket: {session.get('session_id')}")
            
        # Update session timestamp
        session_timestamps[session.get('session_id')] = time.time()
            
        # Send connection confirmation
        emit('connected', {'status': 'success', 'message': 'Connected successfully'})
    except Exception as e:
        logger.error(f"Error in connect handler: {e}")
        emit('error', {'message': 'Connection error'})

@socketio.on('disconnect')
def handle_disconnect():
    try:
        session_id = session.get('session_id')
        logger.info(f"WebSocket disconnect event received for session: {session_id}")
        if session_id and session_id in games:
            # Clean up game instance when user disconnects
            del games[session_id]
            global active_game_count
            active_game_count = max(0, active_game_count - 1)  # Ensure it doesn't go below 0
            logger.info(f"Client disconnected, cleaned up game for session: {session_id}")
            logger.info(f"Active games count: {active_game_count}")
        
        # Send disconnection confirmation
        logger.info("Client disconnected successfully")
    except Exception as e:
        logger.error(f"Error in disconnect handler: {e}")

@socketio.on('init_game')
def handle_init(data):
    start_time = time.time()
    logger.info(f"Game initialization requested with data: {data}")
    logger.info(f"Current session keys: {list(session.keys())}")
    session_id = session.get('session_id')
    logger.info(f"Session ID: {session_id}")
    
    if not session_id:
        logger.error("No session ID found")
        emit('error', {'message': 'Session error'})
        return
    
    try:
        player_color = data.get('color', 'white')
        skill_level = min(20, max(0, int(data.get('level', 5))))
        
        logger.info(f"Creating game with color: {player_color}, skill level: {skill_level}")
        
        # Check if we've reached the maximum concurrent games
        global active_game_count
        if active_game_count >= MAX_CONCURRENT_GAMES:
            logger.warning(f"Maximum concurrent games reached ({MAX_CONCURRENT_GAMES}). Rejecting new game request.")
            emit('error', {'message': 'Server overload. Please try again later.'})
            logger.info(f"Total initialization time: {time.time() - start_time:.2f} seconds")
            return
        
        # Create a new game instance for this session
        game_init_start = time.time()
        game = ChessGame(player_color, skill_level)
        game_init_time = time.time() - game_init_start
        logger.info(f"Game initialization took {game_init_time:.2f} seconds")
        logger.info(f"Game initialization result: {game.initialized}")
        
        if game.initialized:
            games[session_id] = game
            active_game_count += 1
            # Update session timestamp
            session_timestamps[session_id] = time.time()
            fen = game.get_fen()
            logger.info(f"Game initialized successfully. Initial FEN: {fen}")
            logger.info(f"Active games count: {active_game_count}")
            emit('game_initialized', {'fen': fen, 'player_color': player_color})
            logger.info("Sent game_initialized event to client")
            logger.info(f"Total initialization time: {time.time() - start_time:.2f} seconds")
        else:
            logger.error("Failed to initialize Stockfish engine")
            emit('error', {'message': 'Failed to start Stockfish engine'})
            logger.info(f"Total initialization time: {time.time() - start_time:.2f} seconds")
    except Exception as e:
        logger.error(f"Error initializing game: {e}")
        import traceback
        traceback.print_exc()
        emit('error', {'message': 'Game initialization error'})
        logger.info(f"Total initialization time: {time.time() - start_time:.2f} seconds")

@socketio.on('make_move')
def handle_move(data):
    start_time = time.time()
    try:
        logger.info(f"Move request received: {data}")
        logger.info(f"Current session keys: {list(session.keys())}")
        session_id = session.get('session_id')
        logger.info(f"Session ID: {session_id}")
        
        if not session_id or session_id not in games:
            logger.error("Game not initialized for this session")
            emit('error', {'message': 'Game not initialized'})
            return

        game = games[session_id]
        uci_move = data['move']

        # Validate move format
        if not isinstance(uci_move, str) or len(uci_move) != 4:
            emit('invalid_move', {'move': uci_move, 'message': 'Invalid move format'})
            return

        # Validate move using Stockfish
        move_validation_start = time.time()
        is_valid_move = game.is_move_correct(uci_move)
        move_validation_time = time.time() - move_validation_start
        logger.info(f"Move validation took {move_validation_time:.2f} seconds")
        
        if is_valid_move:
            move_execution_start = time.time()
            if not game.make_move(uci_move):
                emit('invalid_move', {'move': uci_move, 'message': 'Invalid move'})
                return
            move_execution_time = time.time() - move_execution_start
            logger.info(f"Move execution took {move_execution_time:.2f} seconds")
                
            fen = game.get_fen()
            
            # Update session timestamp
            session_timestamps[session_id] = time.time()

            # Check game status using improved logic
            game_status_start = time.time()
            game_status = game.get_game_status(fen)
            game_status_time = time.time() - game_status_start
            logger.info(f"Game status check took {game_status_time:.2f} seconds")
            
            if game_status['game_over']:
                emit('game_over', {
                    'result': game_status['result'],
                    'fen': fen,
                    'winner': game_status.get('winner')
                })
                logger.info(f"Total move processing time: {time.time() - start_time:.2f} seconds")
                return

            # AI move
            ai_move_start = time.time()
            ai_move = game.get_best_move()
            ai_move_time = time.time() - ai_move_start
            logger.info(f"AI move calculation took {ai_move_time:.2f} seconds")
            
            if ai_move:
                ai_move_execution_start = time.time()
                if not game.make_move(ai_move):
                    emit('position_update', {'fen': fen})
                    return
                ai_move_execution_time = time.time() - ai_move_execution_start
                logger.info(f"AI move execution took {ai_move_execution_time:.2f} seconds")
                    
                fen = game.get_fen()
                
                # Check game status after AI move
                game_status_start = time.time()
                game_status = game.get_game_status(fen)
                game_status_time = time.time() - game_status_start
                logger.info(f"Post-AI game status check took {game_status_time:.2f} seconds")
                
                if game_status['game_over']:
                    emit('game_over', {
                        'result': game_status['result'],
                        'fen': fen,
                        'winner': game_status.get('winner')
                    })
                    logger.info(f"Total move processing time: {time.time() - start_time:.2f} seconds")
                    return
                    
                emit('position_update', {'fen': fen, 'ai_move': ai_move})
            else:
                emit('position_update', {'fen': fen})
                
            logger.info(f"Total move processing time: {time.time() - start_time:.2f} seconds")
        else:
            emit('invalid_move', {'move': uci_move, 'message': 'Invalid move'})
            logger.info(f"Total move processing time: {time.time() - start_time:.2f} seconds")
    except Exception as e:
        logger.error(f"Error processing move: {e}")
        import traceback
        traceback.print_exc()
        emit('error', {'message': 'Move processing error'})
        logger.info(f"Total move processing time: {time.time() - start_time:.2f} seconds")

if __name__ == '__main__':
    print("DEBUG: Starting Chess Stockfish Web application...")
    socketio.run(app, host='127.0.0.1', port=5001, debug=False)