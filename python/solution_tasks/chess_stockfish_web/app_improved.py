# app_improved.py
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
import pickle
import base64
import functools
from collections import defaultdict

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Store game instances per session
games = {}

# Store game history per session
game_histories = {}

# Store user preferences per session
user_preferences = {}

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

# Cache for expensive operations
cache = {}
CACHE_TTL = 300  # 5 minutes

def cached_result(ttl=CACHE_TTL):
    """Decorator to cache function results"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            current_time = time.time()
            
            # Check if result is in cache and not expired
            if cache_key in cache:
                result, timestamp = cache[cache_key]
                if current_time - timestamp < ttl:
                    logger.debug(f"Cache hit for {func.__name__}")
                    return result
            
            # Call function and cache result
            result = func(*args, **kwargs)
            cache[cache_key] = (result, current_time)
            logger.debug(f"Cache miss for {func.__name__}, cached result")
            return result
        return wrapper
    return decorator

def cleanup_cache():
    """Periodically clean up expired cache entries"""
    global cache
    current_time = time.time()
    expired_keys = [
        key for key, (_, timestamp) in cache.items()
        if current_time - timestamp >= CACHE_TTL
    ]
    for key in expired_keys:
        del cache[key]
    logger.debug(f"Cleaned up {len(expired_keys)} expired cache entries")

def cleanup_stale_games():
    """Periodically clean up stale game sessions to prevent memory leaks."""
    global games, session_timestamps, active_game_count, cache
    while True:
        try:
            time.sleep(CLEANUP_INTERVAL)
            current_time = time.time()
            
            # Clean up cache
            cleanup_cache()
            
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

# Start cleanup thread will be started after all variables are defined

class ChessGame:
    def __init__(self, player_color='white', skill_level=5):
        self.player_color = player_color
        self.skill_level = skill_level
        self.engine = None
        self.initialized = False
        self._fen_cache = None
        self._fen_cache_time = 0
        self._cache_ttl = 1  # 1 second cache for FEN
        self.engine_path = None
        
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
    
    def _find_stockfish_executable(self):
        """Find Stockfish executable in various possible locations"""
        possible_paths = [
            os.path.join(os.path.dirname(__file__), 'stockfish.exe'),  # Local copy
            os.path.join(os.path.dirname(__file__), 'stockfish'),      # Linux/Mac version
            os.path.join(os.path.dirname(__file__), '..', 'stockfish.exe'),  # Parent directory
            os.path.join(os.path.dirname(__file__), '..', 'stockfish'),     # Parent directory (Linux/Mac)
            'stockfish.exe',  # System PATH
            'stockfish',      # System PATH (Linux/Mac)
        ]
        
        # Check environment variable
        env_path = os.getenv('STOCKFISH_PATH')
        if env_path:
            possible_paths.insert(0, env_path)
        
        for path in possible_paths:
            if path and os.path.exists(path):
                logger.info(f"Found Stockfish executable at: {path}")
                return path
        
        logger.warning("Stockfish executable not found in any expected location")
        return None
    
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
            
            # Find Stockfish executable
            self.engine_path = self._find_stockfish_executable()
            if not self.engine_path:
                logger.error("Stockfish executable not found")
                return False
            
            # Initialize new engine
            logger.info(f"Initializing Stockfish engine from: {self.engine_path}")
            self.engine = Stockfish(path=self.engine_path)
            
            # Configure engine for optimal performance
            self.engine.set_skill_level(self.skill_level)
            self.engine.set_depth(10)  # Reduced depth for faster moves, adjustable
            self.engine.update_engine_parameters({
                'Threads': 2,  # Use multiple threads for better performance
                'Hash': 128,   # Allocate 128 MB hash for position evaluation
                'Contempt': 0, # Neutral contempt factor
                'Ponder': False # Disable pondering for faster response
            })
            
            # Test engine with a simple operation
            test_fen = self.engine.get_fen_position()
            logger.info(f"Engine test successful. Initial FEN: {test_fen}")
            
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
    
    @cached_result(ttl=1)  # Cache FEN for 1 second
    def get_fen(self):
        if self.engine:
            try:
                return self.engine.get_fen_position()
            except Exception as e:
                logger.error(f"Error getting FEN position: {e}")
                return None
        return None
    
    def make_move(self, move):
        if not self.initialized or not self.engine:
            logger.error("Engine not initialized")
            return False
        # Clear FEN cache when making a move
        self._fen_cache = None
        try:
            # make_moves_from_current_position returns None on success, False on failure
            result = self.engine.make_moves_from_current_position([move])
            return result is not False
        except Exception as e:
            logger.error(f"Error making move {move}: {e}")
            return False
    
    def is_move_correct(self, move):
        """
        Check if a move is correct using Stockfish's built-in validation for better performance.
        If that fails, fall back to position comparison method.
        """
        if not self.initialized or not self.engine:
            logger.error("Engine not initialized")
            return False
            
        # First try using Stockfish's built-in validation (faster)
        try:
            return self.engine.is_move_correct(move)
        except Exception as e:
            logger.warning(f"Built-in move validation failed: {e}")
            # Fall back to position comparison method if built-in validation fails
            try:
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
            except Exception as e:
                logger.error(f"Position comparison method failed: {e}")
                return False
    
    def get_best_move(self):
        if not self.initialized or not self.engine:
            logger.error("Engine not initialized")
            return None
        try:
            return self.engine.get_best_move()
        except Exception as e:
            logger.error(f"Error getting best move: {e}")
            return None
    
    def get_evaluation(self):
        """Get position evaluation from Stockfish"""
        if not self.initialized or not self.engine:
            logger.error("Engine not initialized")
            return None
        try:
            return self.engine.get_evaluation()
        except Exception as e:
            logger.error(f"Error getting evaluation: {e}")
            return None
    
    def get_top_moves(self, limit=5):
        """Get top moves from Stockfish"""
        if not self.initialized or not self.engine:
            logger.error("Engine not initialized")
            return []
        try:
            return self.engine.get_top_moves(limit)
        except Exception as e:
            logger.error(f"Error getting top moves: {e}")
            return []
    
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
            except Exception as e:
                logger.warning(f"Stockfish evaluation failed: {e}")
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
    logger.info(f"HTTP session created with session_id: {session.get('session_id')}")
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
        emit('error', {'message': 'Ошибка сессии. Попробуйте обновить страницу.'})
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
        
        if game.init_engine():
            games[session_id] = game
            active_game_count += 1
            # Update session timestamp
            if session_id not in session_timestamps:
                session_timestamps[session_id] = time.time()
            else:
                session_timestamps[session_id] = time.time()
            fen = game.get_fen()
            logger.info(f"Game initialized successfully. Initial FEN: {fen}")
            logger.info(f"Active games count: {active_game_count}")
            emit('game_initialized', {'fen': fen, 'player_color': player_color})
            logger.info("Sent game_initialized event to client")
            logger.info(f"Total initialization time: {time.time() - start_time:.2f} seconds")
        else:
            logger.error("Failed to initialize Stockfish engine")
            emit('error', {'message': 'Ошибка движка Stockfish. Попробуйте перезапустить игру.'})
            logger.info(f"Total initialization time: {time.time() - start_time:.2f} seconds")
    except Exception as e:
        logger.error(f"Error initializing game: {e}")
        import traceback
        traceback.print_exc()
        emit('error', {'message': 'Ошибка инициализации игры. Пожалуйста, проверьте консоль для получения дополнительной информации.'})
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
            if session_id not in session_timestamps:
                session_timestamps[session_id] = time.time()
            else:
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
        emit('error', {'message': 'Ошибка обработки хода'})
        logger.info(f"Total move processing time: {time.time() - start_time:.2f} seconds")

@socketio.on('analyze_position')
def handle_analysis(data):
    """Analyze the current position and return evaluation"""
    try:
        session_id = session.get('session_id')
        if not session_id or session_id not in games:
            emit('error', {'message': 'Game not initialized'})
            return

        game = games[session_id]
        fen = data.get('fen', game.get_fen())
        
        if game.engine:
            # Set position for analysis
            game.engine.set_fen_position(fen)
            
            # Get evaluation
            evaluation = game.get_evaluation()
            
            # Get best move for analysis
            best_move = game.get_best_move()
            
            # Get top moves
            top_moves = game.get_top_moves(3)  # Get top 3 moves
            
            emit('analysis_result', {
                'fen': fen,
                'evaluation': evaluation,
                'best_move': best_move,
                'top_moves': top_moves
            })
        else:
            emit('error', {'message': 'Engine not available'})
    except Exception as e:
        logger.error(f"Error in analysis: {e}")
        emit('error', {'message': 'Ошибка анализа позиции'})

@socketio.on('save_preferences')
def handle_save_preferences(data):
    """Save user preferences"""
    try:
        session_id = session.get('session_id')
        if not session_id:
            emit('error', {'message': 'Session not found'})
            return
            
        # Store preferences
        user_preferences[session_id] = data.get('preferences', {})
        
        emit('preferences_saved', {
            'success': True,
            'message': 'Настройки сохранены успешно'
        })
    except Exception as e:
        logger.error(f"Error saving preferences: {e}")
        emit('error', {'message': 'Ошибка сохранения настроек'})

@socketio.on('load_preferences')
def handle_load_preferences():
    """Load user preferences"""
    try:
        session_id = session.get('session_id')
        if not session_id:
            emit('error', {'message': 'Session not found'})
            return
            
        # Get preferences
        preferences = user_preferences.get(session_id, {})
        
        emit('preferences_loaded', {
            'preferences': preferences
        })
    except Exception as e:
        logger.error(f"Error loading preferences: {e}")
        emit('error', {'message': 'Ошибка загрузки настроек'})

@socketio.on('save_game')
def handle_save_game(data):
    """Save the current game state"""
    try:
        session_id = session.get('session_id')
        if not session_id or session_id not in games:
            emit('error', {'message': 'Game not initialized'})
            return

        game = games[session_id]
        
        # Create game state object
        game_state = {
            'fen': game.get_fen(),
            'player_color': game.player_color,
            'skill_level': game.skill_level,
            'game_history': game_histories.get(session_id, []) if session_id in game_histories else [],
            'timestamp': time.time()
        }
        
        # Serialize game state
        serialized_state = base64.b64encode(pickle.dumps(game_state)).decode('utf-8')
        
        emit('game_saved', {
            'success': True,
            'game_state': serialized_state,
            'message': 'Игра сохранена успешно'
        })
    except Exception as e:
        logger.error(f"Error saving game: {e}")
        emit('error', {'message': 'Ошибка сохранения игры'})

@socketio.on('load_game')
def handle_load_game(data):
    """Load a saved game state"""
    try:
        session_id = session.get('session_id')
        serialized_state = data.get('game_state')
        
        if not serialized_state:
            emit('error', {'message': 'Нет данных для загрузки'})
            return
        
        # Deserialize game state
        game_state = pickle.loads(base64.b64decode(serialized_state.encode('utf-8')))
        
        # Create new game instance with saved parameters
        game = ChessGame(game_state['player_color'], game_state['skill_level'])
        
        # Initialize engine
        if not game.init_engine():
            emit('error', {'message': 'Не удалось инициализировать движок'})
            return
            
        # Set position
        if game.engine:
            game.engine.set_fen_position(game_state['fen'])
            game.initialized = True
            
            # Store game in session
            games[session_id] = game
            
            # Update session timestamp
            session_timestamps[session_id] = time.time()
            
            emit('game_loaded', {
                'fen': game_state['fen'],
                'player_color': game_state['player_color'],
                'skill_level': game_state['skill_level'],
                'game_history': game_state.get('game_history', []),
                'message': 'Игра загружена успешно'
            })
        else:
            emit('error', {'message': 'Не удалось инициализировать движок'})
    except Exception as e:
        logger.error(f"Error loading game: {e}")
        emit('error', {'message': 'Ошибка загрузки игры'})

# Start cleanup thread
cleanup_thread = threading.Thread(target=cleanup_stale_games, daemon=True)
cleanup_thread.start()

if __name__ == '__main__':
    logger.info("Starting Chess Stockfish Web application...")
    socketio.run(app, host='127.0.0.1', port=5001, debug=False)