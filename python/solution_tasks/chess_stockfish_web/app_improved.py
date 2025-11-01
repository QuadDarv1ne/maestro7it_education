# app_improved.py
from flask import Flask, render_template, session, request, redirect, url_for, jsonify
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
from collections import defaultdict, OrderedDict
from contextlib import contextmanager
from datetime import datetime

# Import database models
try:
    from models import db, init_db, User, Game, Puzzle, create_user
    DATABASE_ENABLED = True
except ImportError as e:
    print(f"Database models import failed: {e}")
    DATABASE_ENABLED = False
    db = None
    init_db = None
    User = None
    Game = None
    Puzzle = None
    create_user = None

# Import performance tracking
try:
    from utils.performance_tracker import performance_tracker, track_engine_init, track_move_validation, track_move_execution, track_ai_calculation, track_game_status_check, track_fen_retrieval
    PERFORMANCE_TRACKING_ENABLED = True
except ImportError:
    # Fallback if utils module is not available
    PERFORMANCE_TRACKING_ENABLED = False
    performance_tracker = None
    def track_engine_init(func): return func
    def track_move_validation(func): return func
    def track_move_execution(func): return func
    def track_ai_calculation(func): return func
    def track_game_status_check(func): return func
    def track_fen_retrieval(func): return func

# Import cache manager
try:
    from utils.cache_manager import cache_manager, cached
    CACHE_MANAGER_ENABLED = True
except ImportError:
    # Fallback if cache manager is not available
    CACHE_MANAGER_ENABLED = False
    cache_manager = None
    def cached(cache_type='generic'): 
        def decorator(func):
            return func
        return decorator

# Import error handler
try:
    from utils.error_handler import error_handler, handle_chess_errors, retry_on_failure
    # Import exception classes
    from utils.error_handler import EngineInitializationError as ErrorHandlerEngineInitializationError
    from utils.error_handler import MoveValidationError as ErrorHandlerMoveValidationError
    from utils.error_handler import GameLogicError as ErrorHandlerGameLogicError
    ERROR_HANDLER_ENABLED = True
except ImportError:
    # Fallback if error handler is not available
    ERROR_HANDLER_ENABLED = False
    error_handler = None
    def handle_chess_errors(context=""): 
        def decorator(func):
            return func
        return decorator
    def retry_on_failure(max_attempts=3, delay=1.0, backoff=2.0):
        def decorator(func):
            return func
        return decorator
    # Define local exception classes
    class EngineInitializationError(Exception):
        pass
    class MoveValidationError(Exception):
        pass
    class GameLogicError(Exception):
        pass

# Import connection pool
try:
    from utils.connection_pool import stockfish_pool
    CONNECTION_POOLING_ENABLED = True
    # Import the context manager function
    from utils.connection_pool import get_stockfish_engine as pool_get_stockfish_engine
except ImportError:
    # Fallback if connection pool is not available
    CONNECTION_POOLING_ENABLED = False
    stockfish_pool = None
    def pool_get_stockfish_engine(skill_level=5):
        # Simple context manager that creates a new engine each time
        @contextmanager
        def engine_context_manager():
            # Create new engine
            engine_path = _find_stockfish_executable()
            if not engine_path:
                raise EngineInitializationError("Stockfish executable not found")
            
            engine = Stockfish(path=engine_path)
            engine.set_skill_level(skill_level)
            engine.set_depth(10)
            engine.update_engine_parameters({
                'Threads': 2,
                'Hash': 128,
                'Contempt': 0,
                'Ponder': False
            })
            try:
                yield engine
            finally:
                # Clean up engine
                try:
                    # Stockfish doesn't have quit() or close() methods, just let it be garbage collected
                    pass
                except:
                    pass
        return engine_context_manager()
    
    def _find_stockfish_executable():
        """Find Stockfish executable in various possible locations"""
        import shutil
        executable_names = [
            'stockfish.exe',    # Windows
            'stockfish',        # Linux/Mac
            'stockfish_15_x64.exe',
            'stockfish_14_x64.exe',
            'stockfish-windows-x86-64.exe',
            'stockfish-linux-x64',
            'stockfish-mac-x64'
        ]
        
        search_paths = [
            os.path.dirname(__file__),
            os.path.join(os.path.dirname(__file__), '..'),
            os.path.join(os.path.dirname(__file__), 'engines'),
            os.path.expanduser('~'),
            os.path.expanduser('~/stockfish'),
            '/usr/local/bin',
            '/usr/bin',
            'C:\\Program Files\\Stockfish',
            'C:\\Program Files (x86)\\Stockfish'
        ]
        
        # Check environment variable
        env_path = os.getenv('STOCKFISH_PATH')
        if env_path:
            search_paths.insert(0, env_path)
        
        # Try to find executable
        for search_path in search_paths:
            if search_path and os.path.exists(search_path):
                # Check direct path first
                if os.path.isfile(search_path) and any(search_path.endswith(ext) for ext in ['.exe', '']):
                    return search_path
                
                # Check in directory
                for exe_name in executable_names:
                    full_path = os.path.join(search_path, exe_name)
                    if os.path.exists(full_path) and os.access(full_path, os.X_OK):
                        return full_path
        
        # Check system PATH
        for exe_name in executable_names:
            try:
                path = shutil.which(exe_name)
                if path:
                    return path
            except:
                pass
        
        return None

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

def cleanup_stale_games():
    """Periodically clean up stale game sessions to prevent memory leaks."""
    global games, session_timestamps, active_game_count
    while True:
        try:
            time.sleep(CLEANUP_INTERVAL)
            current_time = time.time()
            
            # Find stale sessions
            try:
                stale_sessions = [
                    session_id for session_id, timestamp in session_timestamps.items()
                    if current_time - timestamp > GAME_TIMEOUT
                ]
            except Exception as e:
                logger.error(f"Error finding stale sessions: {e}")
                stale_sessions = []
            
            # Clean up stale sessions
            for session_id in stale_sessions:
                try:
                    if session_id in games:
                        # Clean up game resources
                        try:
                            del games[session_id]
                            active_game_count = max(0, active_game_count - 1)
                            logger.info(f"Cleaned up stale game for session: {session_id}")
                        except Exception as e:
                            logger.error(f"Error cleaning up stale game for session {session_id}: {e}")
                except Exception as e:
                    logger.error(f"Error processing session {session_id}: {e}")
                
                # Remove timestamp
                try:
                    if session_id in session_timestamps:
                        del session_timestamps[session_id]
                except Exception as e:
                    logger.error(f"Error removing timestamp for session {session_id}: {e}")
            
            # Clear expired cache entries
            if CACHE_MANAGER_ENABLED:
                # The cache manager automatically handles TTL expiration
                pass
            
            logger.info(f"Cleanup completed. Active games: {active_game_count}, Tracked sessions: {len(session_timestamps)}")
        except Exception as e:
            logger.error(f"Error in cleanup thread: {e}")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'maestro7it-chess-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///chess.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database if enabled
if DATABASE_ENABLED and init_db:
    db = init_db(app)

socketio = SocketIO(app, cors_allowed_origins="*", ping_timeout=30, ping_interval=25)

# Start cleanup thread after all variables are defined to prevent race conditions

class ChessGame:
    def __init__(self, player_color='white', skill_level=5):
        self.player_color = player_color
        self.skill_level = skill_level
        self.engine = None
        self.initialized = False
        self.engine_path = None
        self._engine_context = None
        self.last_move = None  # Track the last move made
        self.move_history = []  # Track move history for takeback functionality
        self._fen_cache = None  # Cache FEN position
        self._fen_cache_timestamp = 0
        self._fen_cache_ttl = 0.5  # 500ms cache for FEN positions
    
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
        """Find Stockfish executable in various possible locations with enhanced detection"""
        # Common executable names for different platforms
        executable_names = [
            'stockfish.exe',    # Windows
            'stockfish',        # Linux/Mac
            'stockfish_15_x64.exe',  # Specific versions
            'stockfish_14_x64.exe',
            'stockfish_13_x64.exe',
            'stockfish-windows-x86-64.exe',
            'stockfish-linux-x64',
            'stockfish-mac-x64'
        ]
        
        # Common search paths
        search_paths = [
            os.path.dirname(__file__),  # Current directory
            os.path.join(os.path.dirname(__file__), '..'),  # Parent directory
            os.path.join(os.path.dirname(__file__), 'engines'),  # Engines subdirectory
            os.path.join(os.path.dirname(__file__), '..', 'engines'),  # Engines in parent
            os.path.expanduser('~'),  # Home directory
            os.path.expanduser('~/stockfish'),  # Stockfish in home directory
            '/usr/local/bin',  # Common Unix paths
            '/usr/bin',
            'C:\\Program Files\\Stockfish',
            'C:\\Program Files (x86)\\Stockfish'
        ]
        
        # Check environment variable
        env_path = os.getenv('STOCKFISH_PATH')
        if env_path:
            search_paths.insert(0, env_path)
        
        # Try to find executable in search paths
        import shutil
        for search_path in search_paths:
            if search_path and os.path.exists(search_path):
                # Check direct path first
                if os.path.isfile(search_path) and any(search_path.endswith(ext) for ext in ['.exe', '']):
                    logger.info(f"Found Stockfish executable at direct path: {search_path}")
                    return search_path
                
                # Check in directory
                for exe_name in executable_names:
                    full_path = os.path.join(search_path, exe_name)
                    if os.path.exists(full_path) and os.access(full_path, os.X_OK):
                        logger.info(f"Found Stockfish executable at: {full_path}")
                        return full_path
        
        # Check system PATH
        for exe_name in executable_names:
            try:
                path = shutil.which(exe_name)
                if path:
                    logger.info(f"Found Stockfish executable in PATH: {path}")
                    return path
            except:
                pass
        
        logger.warning("Stockfish executable not found in any expected location")
        return None
    
    @retry_on_failure(max_attempts=3, delay=1.0, backoff=2.0)
    @track_engine_init
    @handle_chess_errors(context="engine_initialization")
    def init_engine(self):
        global stockfish_engine
        start_time = time.time()
        try:
            # Use connection pooling if available
            if CONNECTION_POOLING_ENABLED and stockfish_pool:
                # Get engine from pool using context manager
                self._engine_context = pool_get_stockfish_engine(self.skill_level)
                # Correctly use the context manager
                self.engine = self._engine_context.__enter__()
                self.initialized = True
                logger.info(f"Got Stockfish engine from pool with skill level {self.skill_level} in {time.time() - start_time:.2f} seconds")
                return True
            
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
                raise EngineInitializationError("Stockfish executable not found")
            
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
            # Try to clean up any partially initialized engine
            try:
                if hasattr(self, 'engine') and self.engine:
                    if CONNECTION_POOLING_ENABLED and self._engine_context:
                        try:
                            self._engine_context.__exit__(None, None, None)
                        except:
                            pass
                    else:
                        # Stockfish doesn't have explicit close method, just dereference
                        self.engine = None
            except:
                pass
            self.initialized = False
            raise EngineInitializationError(f"Failed to initialize Stockfish engine: {str(e)}") from e
    
    def __del__(self):
        """Clean up engine when ChessGame instance is destroyed"""
        try:
            if self.initialized and self.engine:
                if CONNECTION_POOLING_ENABLED and self._engine_context:
                    try:
                        self._engine_context.__exit__(None, None, None)
                    except:
                        pass
                # Stockfish doesn't have explicit cleanup methods
                self.engine = None
        except Exception as e:
            logger.warning(f"Error cleaning up engine: {e}")
    
    @cached('board_state')
    @track_fen_retrieval
    @handle_chess_errors(context="fen_retrieval")
    def get_fen(self):
        if self.engine and self.initialized:
            try:
                # Check cache first
                current_time = time.time()
                if (self._fen_cache and 
                    current_time - self._fen_cache_timestamp < self._fen_cache_ttl):
                    return self._fen_cache
                
                fen = self.engine.get_fen_position()
                if fen is None:
                    logger.warning("Stockfish returned None for FEN position")
                
                # Update cache
                self._fen_cache = fen
                self._fen_cache_timestamp = current_time
                
                return fen
            except Exception as e:
                logger.error(f"Error getting FEN position: {e}")
                raise GameLogicError(f"Failed to get FEN position: {str(e)}") from e
        else:
            logger.warning("Engine not initialized when trying to get FEN")
            raise EngineInitializationError("Engine not initialized")
        return None
    
    @track_move_execution
    @handle_chess_errors(context="move_execution")
    def make_move(self, move):
        if not self.initialized or not self.engine:
            logger.error("Engine not initialized")
            raise EngineInitializationError("Engine not initialized")
        # Validate move format
        if not isinstance(move, str) or len(move) != 4:
            logger.error(f"Invalid move format: {move}")
            raise MoveValidationError(f"Invalid move format: {move}")
        try:
            # Clear FEN cache as position will change
            self._fen_cache = None
            
            # make_moves_from_current_position returns None on success, False on failure
            result = self.engine.make_moves_from_current_position([move])
            success = result is not False
            if not success:
                logger.warning(f"Move {move} was rejected by Stockfish engine")
                raise MoveValidationError(f"Move {move} was rejected by Stockfish engine")
            return success
        except MoveValidationError:
            raise
        except Exception as e:
            logger.error(f"Error making move {move}: {e}")
            raise GameLogicError(f"Failed to execute move {move}: {str(e)}") from e
    
    @cached('valid_moves')
    @track_move_validation
    @handle_chess_errors(context="move_validation")
    def is_move_correct(self, move):
        """
        Check if a move is correct using Stockfish's built-in validation for better performance.
        If that fails, fall back to position comparison method.
        """
        if not self.initialized or not self.engine:
            logger.error("Engine not initialized")
            raise EngineInitializationError("Engine not initialized")
            
        # Validate move format first
        if not isinstance(move, str) or len(move) != 4:
            logger.warning(f"Invalid move format: {move}")
            raise MoveValidationError(f"Invalid move format: {move}")
            
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
                raise MoveValidationError(f"Failed to validate move {move}: {str(e)}") from e
    
    @cached('ai_move')
    @track_ai_calculation
    @handle_chess_errors(context="ai_move_calculation")
    @retry_on_failure(max_attempts=2, delay=0.5, backoff=1.5)
    def get_best_move(self):
        if not self.initialized or not self.engine:
            logger.error("Engine not initialized")
            raise EngineInitializationError("Engine not initialized")
        try:
            best_move = self.engine.get_best_move()
            if best_move is None:
                logger.warning("Stockfish returned None for best move")
            return best_move
        except Exception as e:
            logger.error(f"Error getting best move: {e}")
            raise GameLogicError(f"Failed to get best move: {str(e)}") from e
    
    @cached('evaluation')
    @handle_chess_errors(context="position_evaluation")
    def get_evaluation(self):
        """Get position evaluation from Stockfish"""
        if not self.initialized or not self.engine:
            logger.error("Engine not initialized")
            raise EngineInitializationError("Engine not initialized")
        try:
            return self.engine.get_evaluation()
        except Exception as e:
            logger.error(f"Error getting evaluation: {e}")
            raise GameLogicError(f"Failed to get position evaluation: {str(e)}") from e
    
    @cached('valid_moves')
    @handle_chess_errors(context="top_moves")
    def get_top_moves(self, limit=5):
        """Get top moves from Stockfish"""
        if not self.initialized or not self.engine:
            logger.error("Engine not initialized")
            raise EngineInitializationError("Engine not initialized")
        try:
            return self.engine.get_top_moves(limit)
        except Exception as e:
            logger.error(f"Error getting top moves: {e}")
            raise GameLogicError(f"Failed to get top moves: {str(e)}") from e
    
    @cached('game_status')
    @track_game_status_check
    @handle_chess_errors(context="game_status_check")
    def get_game_status(self, fen):
        """
        Determine the game status (check, checkmate, stalemate) from the FEN string.
        Returns a dictionary with game status information.
        """
        if not fen:
            return {'game_over': False}
        
        # Check for checkmate using Stockfish evaluation
        if self.engine and self.initialized:
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
                        best_move = self.engine.get_best_move()
                        if not best_move:
                            return {
                                'game_over': True,
                                'result': 'stalemate'
                            }
            except Exception as e:
                logger.warning(f"Stockfish evaluation failed: {e}")
                # Fallback to FEN-based detection if evaluation fails
                pass
        
        # Fallback to original FEN-based detection
        try:
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
        except Exception as e:
            logger.warning(f"FEN-based game status detection failed: {e}")
            pass
        
        return {'game_over': False}

@app.route('/')
def index():
    # Generate a unique session ID for each user
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    logger.info(f"HTTP session created with session_id: {session.get('session_id')}")
    return render_template('index.html')

@app.route('/profile_page')
def profile_page():
    """Serve the profile page"""
    # Check if user is logged in
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('index'))
    
    return render_template('profile.html')

@socketio.on('connect')
@handle_chess_errors(context="websocket_connect")
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
            
        # Update session timestamp with existence check
        session_id = session.get('session_id')
        if session_id:
            if session_id not in session_timestamps:
                session_timestamps[session_id] = time.time()
            else:
                session_timestamps[session_id] = time.time()
            
        # Send connection confirmation
        emit('connected', {'status': 'success', 'message': 'Connected successfully'})
    except Exception as e:
        logger.error(f"Error in connect handler: {e}")
        emit('error', {'message': 'Connection error'})

@socketio.on('disconnect')
@handle_chess_errors(context="websocket_disconnect")
def handle_disconnect():
    try:
        session_id = session.get('session_id')
        logger.info(f"WebSocket disconnect event received for session: {session_id}")
        if session_id:
            if session_id in games:
                # Clean up game instance when user disconnects
                del games[session_id]
                global active_game_count
                active_game_count = max(0, active_game_count - 1)  # Ensure it doesn't go below 0
                logger.info(f"Client disconnected, cleaned up game for session: {session_id}")
                logger.info(f"Active games count: {active_game_count}")
            
            # Remove timestamp
            if session_id in session_timestamps:
                del session_timestamps[session_id]
                logger.info(f"Removed timestamp for session: {session_id}")
        
        # Send disconnection confirmation
        logger.info("Client disconnected successfully")
    except Exception as e:
        logger.error(f"Error in disconnect handler: {e}")

# Add this after the existing routes and before the health check endpoint

@app.route('/register', methods=['POST'])
@handle_chess_errors(context="user_registration")
def register_user():
    """Register a new user"""
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        # Validate input
        if not username or not email or not password:
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        # Check if database is enabled and models are available
        if not DATABASE_ENABLED or User is None or db is None:
            return jsonify({'success': False, 'message': 'Database not enabled'}), 500
        
        # Check if user already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            return jsonify({'success': False, 'message': 'User already exists'}), 400
        
        # Create new user (in a real app, you would hash the password)
        if create_user is not None:
            user = create_user(username, email, password)  # Password hashing should be added in production
            return jsonify({'success': True, 'message': 'User registered successfully', 'user_id': user.id})
        else:
            return jsonify({'success': False, 'message': 'User creation failed'}), 500
    except Exception as e:
        logger.error(f"Error registering user: {e}")
        return jsonify({'success': False, 'message': 'Registration failed'}), 500

@app.route('/login', methods=['POST'])
@handle_chess_errors(context="user_login")
def login_user():
    """Login a user"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        # Validate input
        if not username or not password:
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        # Check if database is enabled and models are available
        if not DATABASE_ENABLED or User is None or db is None:
            return jsonify({'success': False, 'message': 'Database not enabled'}), 500
        
        # Check if user exists
        user = User.query.filter(User.username == username).first() if User is not None else None
        if user and user.password_hash == password:  # In production, use proper password hashing
            # Update last login
            user.last_login = datetime.utcnow()
            if db is not None:
                db.session.commit()
            
            # Store user ID in session
            session['user_id'] = user.id
            
            return jsonify({
                'success': True, 
                'message': 'Login successful', 
                'user_id': user.id,
                'username': user.username
            })
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    except Exception as e:
        logger.error(f"Error logging in user: {e}")
        return jsonify({'success': False, 'message': 'Login failed'}), 500

@app.route('/logout')
@handle_chess_errors(context="user_logout")
def logout_user():
    """Logout a user"""
    try:
        # Remove user ID from session
        session.pop('user_id', None)
        return jsonify({'success': True, 'message': 'Logout successful'})
    except Exception as e:
        logger.error(f"Error logging out user: {e}")
        return jsonify({'success': False, 'message': 'Logout failed'}), 500

@app.route('/profile')
@handle_chess_errors(context="user_profile")
def user_profile():
    """Display user profile"""
    try:
        # Check if user is logged in
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'success': False, 'message': 'User not logged in'}), 401
        
        # Check if database is enabled
        if not DATABASE_ENABLED or User is None or Game is None:
            return jsonify({'success': False, 'message': 'Database not enabled'}), 500
        
        # Get user information
        user = User.query.get(user_id) if User is not None else None
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        # Get user's recent games
        recent_games = Game.query.filter_by(user_id=user_id).order_by(Game.start_time.desc()).limit(10).all() if Game is not None else []
        
        # Calculate statistics
        total_games = user.games_played or 0
        wins = user.games_won or 0
        losses = total_games - wins
        win_rate = (wins / total_games * 100) if total_games > 0 else 0
        
        # Prepare game history data
        game_history = []
        for game in recent_games:
            game_history.append({
                'id': game.id,
                'result': game.result,
                'player_color': game.player_color,
                'skill_level': game.skill_level,
                'start_time': game.start_time.isoformat() if game.start_time else None,
                'duration': game.duration
            })
        
        return jsonify({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'rating': user.rating or 1200,
                'games_played': total_games,
                'wins': wins,
                'losses': losses,
                'win_rate': round(win_rate, 2)
            },
            'recent_games': game_history
        })
    except Exception as e:
        logger.error(f"Error fetching user profile: {e}")
        return jsonify({'success': False, 'message': 'Failed to fetch profile'}), 500

# Add health check endpoint
@app.route('/health')
@handle_chess_errors(context="health_check")
def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Check if we can create a simple ChessGame instance
        game = ChessGame()
        
        # Get cache statistics if cache manager is enabled
        cache_stats = {}
        if CACHE_MANAGER_ENABLED and cache_manager:
            cache_stats = cache_manager.get_cache_stats()
        
        # Get performance metrics if performance tracking is enabled
        perf_metrics = {}
        if PERFORMANCE_TRACKING_ENABLED and performance_tracker:
            perf_metrics = performance_tracker.get_metrics_summary()
        
        # Get error statistics if error handler is enabled
        error_stats = {}
        if ERROR_HANDLER_ENABLED and error_handler:
            error_stats = error_handler.get_error_stats()
        
        # Get connection pool statistics if connection pooling is enabled
        pool_stats = {}
        if CONNECTION_POOLING_ENABLED and stockfish_pool:
            pool_stats = stockfish_pool.get_stats()
        
        return {
            'status': 'healthy',
            'active_games': active_game_count,
            'tracked_sessions': len(session_timestamps),
            'cache_stats': cache_stats,
            'performance_metrics': perf_metrics,
            'error_stats': error_stats,
            'pool_stats': pool_stats
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {'status': 'unhealthy', 'error': str(e)}, 500

@socketio.on('init_game')
@handle_chess_errors(context="game_initialization")
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
            total_init_time = time.time() - start_time
            logger.info(f"Total initialization time: {total_init_time:.2f} seconds")
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
            if fen is None:
                logger.error("Failed to get initial FEN position")
                emit('error', {'message': 'Ошибка получения начальной позиции. Попробуйте перезапустить игру.'})
                # Clean up
                if session_id in games:
                    del games[session_id]
                    active_game_count -= 1
                return
            logger.info(f"Game initialized successfully. Initial FEN: {fen}")
            logger.info(f"Active games count: {active_game_count}")
            
            # Save game to database if user is logged in and database is enabled
            game_id = None
            user_id = session.get('user_id')
            if DATABASE_ENABLED and user_id and Game is not None and db is not None:
                try:
                    db_game = Game(
                        user_id=user_id,
                        fen=fen,
                        player_color=player_color,
                        skill_level=skill_level,
                        result='in_progress'
                    )
                    if db is not None:
                        db.session.add(db_game)
                        db.session.commit()
                        game_id = db_game.id
                        logger.info(f"Game saved to database with ID: {game_id}")
                except Exception as e:
                    logger.error(f"Failed to save game to database: {e}")
            
            emit('game_initialized', {'fen': fen, 'player_color': player_color, 'game_id': game_id})
            logger.info("Sent game_initialized event to client")
            total_init_time = time.time() - start_time
            logger.info(f"Total initialization time: {total_init_time:.2f} seconds")
        else:
            logger.error("Failed to initialize Stockfish engine")
            emit('error', {'message': 'Ошибка движка Stockfish. Попробуйте перезапустить игру.'})
            total_init_time = time.time() - start_time
            logger.info(f"Total initialization time: {total_init_time:.2f} seconds")
    except EngineInitializationError as e:
        logger.error(f"Engine initialization error: {e}")
        emit('error', {'message': 'Ошибка движка Stockfish. Попробуйте перезапустить игру.'})
        # Re-enable start button on error
        try:
            emit('enable_start_button')
        except:
            pass  # Ignore if client is not connected
        total_init_time = time.time() - start_time
        logger.info(f"Total initialization time: {total_init_time:.2f} seconds")
    except Exception as e:
        logger.error(f"Error initializing game: {e}")
        import traceback
        traceback.print_exc()
        emit('error', {'message': 'Ошибка инициализации игры. Пожалуйста, проверьте консоль для получения дополнительной информации.'})
        # Re-enable start button on error
        try:
            emit('enable_start_button')
        except:
            pass  # Ignore if client is not connected
        total_init_time = time.time() - start_time
        logger.info(f"Total initialization time: {total_init_time:.2f} seconds")

@socketio.on('make_move')
@handle_chess_errors(context="move_processing")
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
        uci_move = data.get('move')
        
        # Validate move exists
        if not uci_move:
            logger.error("No move provided in request")
            emit('invalid_move', {'move': '', 'message': 'No move provided'})
            return

        # Validate move format
        if not isinstance(uci_move, str) or len(uci_move) != 4:
            logger.warning(f"Invalid move format: {uci_move}")
            emit('invalid_move', {'move': uci_move, 'message': 'Invalid move format'})
            return

        # Store the move as the last move
        game.last_move = uci_move

        # Validate move using Stockfish
        move_validation_start = time.time()
        is_valid_move = game.is_move_correct(uci_move)
        move_validation_time = time.time() - move_validation_start
        logger.info(f"Move validation took {move_validation_time:.2f} seconds")
        
        if is_valid_move:
            move_execution_start = time.time()
            if not game.make_move(uci_move):
                logger.warning(f"Move execution failed for move: {uci_move}")
                emit('invalid_move', {'move': uci_move, 'message': 'Invalid move'})
                return
            move_execution_time = time.time() - move_execution_start
            logger.info(f"Move execution took {move_execution_time:.2f} seconds")
                
            # Add move to history
            game.move_history.append(uci_move)
                
            fen = game.get_fen()
            if fen is None:
                logger.error("Failed to get FEN after move execution")
                emit('error', {'message': 'Ошибка получения позиции после хода'})
                return
            
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
                # Update game result in database if user is logged in and database is enabled
                user_id = session.get('user_id')
                if DATABASE_ENABLED and user_id and Game is not None and db is not None:
                    try:
                        # Find the game in the database
                        db_game = Game.query.filter_by(user_id=user_id, result='in_progress').order_by(Game.start_time.desc()).first()
                        if db_game:
                            # Update game result
                            db_game.result = game_status['result']
                            db_game.end_time = datetime.utcnow()
                            db_game.duration = int((db_game.end_time - db_game.start_time).total_seconds()) if db_game.start_time else 0
                            db_game.move_history = json.dumps(game.move_history) if game.move_history else None
                            
                            # Update user stats
                            user = User.query.get(user_id) if User is not None else None
                            if user:
                                user.games_played = (user.games_played or 0) + 1
                                if game_status.get('winner') == game.player_color:
                                    user.games_won = (user.games_won or 0) + 1
                                    # Simple rating update - in a real app, you'd use a proper rating system
                                    user.rating = (user.rating or 1200) + 10
                                elif game_status['result'] == 'stalemate':
                                    # No rating change for stalemate
                                    pass
                                else:
                                    # Loss - decrease rating
                                    user.rating = max(100, (user.rating or 1200) - 5)
                            
                            db.session.commit()
                            logger.info(f"Game result saved to database: {game_status['result']}")
                    except Exception as e:
                        logger.error(f"Failed to save game result to database: {e}")
                
                emit('game_over', {
                    'result': game_status['result'],
                    'fen': fen,
                    'winner': game_status.get('winner'),
                    'last_move': game.last_move
                })
                total_move_time = time.time() - start_time
                logger.info(f"Total move processing time: {total_move_time:.2f} seconds")
                return

            # AI move
            ai_move_start = time.time()
            ai_move = game.get_best_move()
            ai_move_time = time.time() - ai_move_start
            logger.info(f"AI move calculation took {ai_move_time:.2f} seconds")
            
            if ai_move:
                # Store AI move as the last move
                game.last_move = ai_move
                
                ai_move_execution_start = time.time()
                if not game.make_move(ai_move):
                    logger.warning(f"AI move execution failed for move: {ai_move}")
                    emit('position_update', {'fen': fen, 'last_move': game.last_move})
                    return
                ai_move_execution_time = time.time() - ai_move_execution_start
                logger.info(f"AI move execution took {ai_move_execution_time:.2f} seconds")
                    
                # Add AI move to history
                game.move_history.append(ai_move)
                    
                fen = game.get_fen()
                if fen is None:
                    logger.error("Failed to get FEN after AI move execution")
                    emit('error', {'message': 'Ошибка получения позиции после хода компьютера'})
                    return
                
                # Check game status after AI move
                game_status_start = time.time()
                game_status = game.get_game_status(fen)
                game_status_time = time.time() - game_status_start
                logger.info(f"Post-AI game status check took {game_status_time:.2f} seconds")
                
                if game_status['game_over']:
                    # Update game result in database if user is logged in and database is enabled
                    user_id = session.get('user_id')
                    if DATABASE_ENABLED and user_id and Game is not None and db is not None:
                        try:
                            # Find the game in the database
                            db_game = Game.query.filter_by(user_id=user_id, result='in_progress').order_by(Game.start_time.desc()).first()
                            if db_game:
                                # Update game result
                                db_game.result = game_status['result']
                                db_game.end_time = datetime.utcnow()
                                db_game.duration = int((db_game.end_time - db_game.start_time).total_seconds()) if db_game.start_time else 0
                                db_game.move_history = json.dumps(game.move_history) if game.move_history else None
                                
                                # Update user stats
                                user = User.query.get(user_id) if User is not None else None
                                if user and User is not None:
                                    user.games_played = (user.games_played or 0) + 1
                                    if game_status.get('winner') == game.player_color:
                                        user.games_won = (user.games_won or 0) + 1
                                        # Simple rating update - in a real app, you'd use a proper rating system
                                        user.rating = (user.rating or 1200) + 10
                                    elif game_status['result'] == 'stalemate':
                                        # No rating change for stalemate
                                        pass
                                    else:
                                        # Loss - decrease rating
                                        user.rating = max(100, (user.rating or 1200) - 5)
                                
                                db.session.commit()
                                logger.info(f"Game result saved to database: {game_status['result']}")
                        except Exception as e:
                            logger.error(f"Failed to save game result to database: {e}")
                    
                    emit('game_over', {
                        'result': game_status['result'],
                        'fen': fen,
                        'winner': game_status.get('winner'),
                        'last_move': game.last_move
                    })
                    total_move_time = time.time() - start_time
                    logger.info(f"Total move processing time: {total_move_time:.2f} seconds")
                    return
                    
                emit('position_update', {'fen': fen, 'ai_move': ai_move, 'last_move': game.last_move})
            else:
                logger.warning("No AI move available")
                emit('position_update', {'fen': fen, 'last_move': game.last_move})
                
            total_move_time = time.time() - start_time
            logger.info(f"Total move processing time: {total_move_time:.2f} seconds")
        else:
            logger.warning(f"Invalid move: {uci_move}")
            emit('invalid_move', {'move': uci_move, 'message': 'Invalid move'})
            total_move_time = time.time() - start_time
            logger.info(f"Total move processing time: {total_move_time:.2f} seconds")
    except MoveValidationError as e:
        logger.warning(f"Move validation error: {e}")
        emit('invalid_move', {'move': data.get('move', ''), 'message': str(e)})
        total_move_time = time.time() - start_time
        logger.info(f"Total move processing time: {total_move_time:.2f} seconds")
    except EngineInitializationError as e:
        logger.error(f"Engine error during move processing: {e}")
        emit('error', {'message': 'Ошибка движка. Попробуйте перезапустить игру.'})
        total_move_time = time.time() - start_time
        logger.info(f"Total move processing time: {total_move_time:.2f} seconds")
    except GameLogicError as e:
        logger.error(f"Game logic error: {e}")
        emit('error', {'message': 'Ошибка обработки хода'})
        total_move_time = time.time() - start_time
        logger.info(f"Total move processing time: {total_move_time:.2f} seconds")
    except Exception as e:
        logger.error(f"Error processing move: {e}")
        import traceback
        traceback.print_exc()
        emit('error', {'message': 'Ошибка обработки хода'})
        total_move_time = time.time() - start_time
        logger.info(f"Total move processing time: {total_move_time:.2f} seconds")

@socketio.on('takeback_move')
@handle_chess_errors(context="move_takeback")
def handle_takeback():
    """Handle takeback move request"""
    try:
        session_id = session.get('session_id')
        if not session_id or session_id not in games:
            emit('error', {'message': 'Game not initialized'})
            return

        game = games[session_id]
        
        if not game.engine or not game.initialized:
            emit('error', {'message': 'Engine not initialized'})
            return
            
        # Check if there are moves to take back
        if len(game.move_history) < 1:
            emit('error', {'message': 'No moves to take back'})
            return
            
        # Remove the last move from history
        last_move = game.move_history.pop()
        
        # Set the engine to the previous position
        if game.move_history:
            # Apply all moves except the last one
            game.engine.set_position(game.move_history)
        else:
            # Reset to starting position
            game.engine.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        
        fen = game.get_fen()
        if fen is None:
            logger.error("Failed to get FEN after takeback")
            emit('error', {'message': 'Ошибка получения позиции после отмены хода'})
            return
            
        # Update session timestamp
        session_timestamps[session_id] = time.time()
        
        emit('position_update', {'fen': fen, 'takeback': True})
        
    except Exception as e:
        logger.error(f"Error processing takeback: {e}")
        import traceback
        traceback.print_exc()
        emit('error', {'message': 'Ошибка отмены хода'})

@socketio.on('analyze_position')
@handle_chess_errors(context="position_analysis")
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
@handle_chess_errors(context="preferences_save")
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
@handle_chess_errors(context="preferences_load")
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
@handle_chess_errors(context="game_save")
def handle_save_game(data):
    """Save the current game state"""
    try:
        session_id = session.get('session_id')
        if not session_id or session_id not in games:
            emit('error', {'message': 'Game not initialized'})
            return

        game = games[session_id]
        
        # Get current FEN
        fen = game.get_fen()
        if fen is None:
            logger.error("Failed to get FEN for game save")
            emit('error', {'message': 'Ошибка получения позиции для сохранения'})
            return
        
        # Create game state object
        game_state = {
            'fen': fen,
            'player_color': game.player_color,
            'skill_level': game.skill_level,
            'game_history': game_histories.get(session_id, []) if session_id in game_histories else [],
            'timestamp': time.time()
        }
        
        # Serialize game state
        try:
            serialized_state = base64.b64encode(pickle.dumps(game_state)).decode('utf-8')
        except Exception as e:
            logger.error(f"Error serializing game state: {e}")
            emit('error', {'message': 'Ошибка сериализации игры'})
            return
        
        emit('game_saved', {
            'success': True,
            'game_state': serialized_state,
            'message': 'Игра сохранена успешно'
        })
    except Exception as e:
        logger.error(f"Error saving game: {e}")
        emit('error', {'message': 'Ошибка сохранения игры'})

@socketio.on('load_game')
@handle_chess_errors(context="game_load")
def handle_load_game(data):
    """Load a saved game state"""
    try:
        session_id = session.get('session_id')
        serialized_state = data.get('game_state')
        
        if not serialized_state:
            emit('error', {'message': 'Нет данных для загрузки'})
            return
        
        # Deserialize game state
        try:
            game_state = pickle.loads(base64.b64decode(serialized_state.encode('utf-8')))
        except Exception as e:
            logger.error(f"Error deserializing game state: {e}")
            emit('error', {'message': 'Ошибка десериализации сохраненной игры'})
            return
        
        # Validate game state
        if not isinstance(game_state, dict):
            logger.error("Invalid game state format")
            emit('error', {'message': 'Неверный формат сохраненной игры'})
            return
            
        required_fields = ['player_color', 'skill_level', 'fen']
        for field in required_fields:
            if field not in game_state:
                logger.error(f"Missing required field in game state: {field}")
                emit('error', {'message': f'Отсутствует обязательное поле: {field}'})
                return
        
        # Create new game instance with saved parameters
        game = ChessGame(game_state['player_color'], game_state['skill_level'])
        
        # Initialize engine
        if not game.init_engine():
            emit('error', {'message': 'Не удалось инициализировать движок'})
            return
            
        # Set position
        if game.engine:
            try:
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
            except Exception as e:
                logger.error(f"Error setting FEN position: {e}")
                emit('error', {'message': 'Ошибка установки позиции доски'})
                return
        else:
            emit('error', {'message': 'Не удалось инициализировать движок'})
    except Exception as e:
        logger.error(f"Error loading game: {e}")
        emit('error', {'message': 'Ошибка загрузки игры'})

@app.route('/pool-stats')
def pool_stats():
    """Endpoint to get connection pool statistics"""
    try:
        # Test connection pooling if enabled
        pool_stats = {}
        if CONNECTION_POOLING_ENABLED and stockfish_pool:
            pool_stats = stockfish_pool.get_stats()
        
        return {
            'status': 'success',
            'connection_pooling_enabled': CONNECTION_POOLING_ENABLED,
            'pool_stats': pool_stats,
            'timestamp': time.time()
        }
    except Exception as e:
        logger.error(f"Pool stats endpoint failed: {e}")
        return {
            'status': 'error',
            'error': str(e)
        }, 500

# Start cleanup thread
cleanup_thread = threading.Thread(target=cleanup_stale_games, daemon=True)
cleanup_thread.start()

if __name__ == '__main__':
    logger.info("Starting Chess Stockfish Web application...")
    
    # Create database tables if they don't exist
    if DATABASE_ENABLED and db is not None:
        with app.app_context():
            db.create_all()
    
    socketio.run(app, host='127.0.0.1', port=5001, debug=False)