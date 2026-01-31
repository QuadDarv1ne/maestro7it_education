#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
WebSocket Server for Real-time Chess Multiplayer
Enables live multiplayer chess games with real-time updates
"""

import asyncio
import websockets
import json
import uuid
from typing import Dict, List, Set
import threading
import time
from dataclasses import dataclass, asdict
from enum import Enum

class GameStatus(Enum):
    WAITING = "waiting"
    PLAYING = "playing"
    FINISHED = "finished"
    ABANDONED = "abandoned"

class PlayerColor(Enum):
    WHITE = "white"
    BLACK = "black"

@dataclass
class Player:
    id: str
    name: str
    websocket: websockets.WebSocketServerProtocol
    color: PlayerColor = None
    ready: bool = False

@dataclass
class ChessGame:
    id: str
    white_player: Player = None
    black_player: Player = None
    status: GameStatus = GameStatus.WAITING
    current_turn: PlayerColor = PlayerColor.WHITE
    board_state: List[List[str]] = None
    move_history: List[Dict] = None
    created_at: float = None
    last_activity: float = None
    
    def __post_init__(self):
        if self.board_state is None:
            self.board_state = self.get_initial_board()
        if self.move_history is None:
            self.move_history = []
        if self.created_at is None:
            self.created_at = time.time()
        if self.last_activity is None:
            self.last_activity = time.time()
    
    def get_initial_board(self):
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
    
    def to_dict(self):
        return {
            'id': self.id,
            'status': self.status.value,
            'current_turn': self.current_turn.value,
            'board_state': self.board_state,
            'move_history': self.move_history,
            'created_at': self.created_at,
            'last_activity': self.last_activity,
            'white_player': self.white_player.name if self.white_player else None,
            'black_player': self.black_player.name if self.black_player else None
        }

class ChessWebSocketServer:
    def __init__(self, host='localhost', port=8765):
        self.host = host
        self.port = port
        self.games: Dict[str, ChessGame] = {}
        self.players: Dict[str, Player] = {}
        self.waiting_players: Set[str] = set()
        self.game_lock = threading.Lock()
        
    async def register_player(self, websocket, player_name):
        """Register a new player"""
        player_id = str(uuid.uuid4())
        player = Player(id=player_id, name=player_name, websocket=websocket)
        self.players[player_id] = player
        self.waiting_players.add(player_id)
        
        # Try to pair with another waiting player
        await self.try_pair_players(player_id)
        
        return player_id
    
    async def try_pair_players(self, player_id):
        """Try to pair a player with another waiting player"""
        with self.game_lock:
            if len(self.waiting_players) >= 2 and player_id in self.waiting_players:
                # Get two waiting players
                waiting_list = list(self.waiting_players)
                player1_id = player_id
                player2_id = next(pid for pid in waiting_list if pid != player_id)
                
                # Remove from waiting list
                self.waiting_players.discard(player1_id)
                self.waiting_players.discard(player2_id)
                
                # Create new game
                game_id = str(uuid.uuid4())
                game = ChessGame(id=game_id)
                
                # Assign players to game
                game.white_player = self.players[player1_id]
                game.black_player = self.players[player2_id]
                game.white_player.color = PlayerColor.WHITE
                game.black_player.color = PlayerColor.BLACK
                game.status = GameStatus.PLAYING
                
                # Add to games
                self.games[game_id] = game
                
                # Notify players
                await self.notify_game_start(game)
    
    async def notify_game_start(self, game):
        """Notify players that the game has started"""
        start_message = {
            'type': 'game_started',
            'game_id': game.id,
            'board_state': game.board_state,
            'your_color': 'white',
            'opponent': game.black_player.name
        }
        await game.white_player.websocket.send(json.dumps(start_message))
        
        start_message['your_color'] = 'black'
        start_message['opponent'] = game.white_player.name
        await game.black_player.websocket.send(json.dumps(start_message))
    
    async def handle_move(self, game_id, player_id, move_data):
        """Handle a move from a player"""
        with self.game_lock:
            if game_id not in self.games:
                return
            
            game = self.games[game_id]
            player = self.players[player_id]
            
            # Validate it's the player's turn
            if ((player.color == PlayerColor.WHITE and game.current_turn != PlayerColor.WHITE) or
                (player.color == PlayerColor.BLACK and game.current_turn != PlayerColor.BLACK)):
                await self.send_error(player.websocket, "Not your turn")
                return
            
            # Validate move (simplified - would integrate with C++ engine in production)
            if self.is_valid_move(game.board_state, move_data):
                # Execute move
                self.execute_move(game.board_state, move_data)
                
                # Add to move history
                move_record = {
                    'player': player.name,
                    'color': player.color.value,
                    'move': move_data,
                    'timestamp': time.time()
                }
                game.move_history.append(move_record)
                
                # Switch turns
                game.current_turn = PlayerColor.BLACK if game.current_turn == PlayerColor.WHITE else PlayerColor.WHITE
                game.last_activity = time.time()
                
                # Notify both players
                await self.broadcast_move(game, move_record)
                
                # Check game end conditions
                await self.check_game_end(game)
            else:
                await self.send_error(player.websocket, "Invalid move")
    
    def is_valid_move(self, board, move_data):
        """Basic move validation (would integrate with C++ engine)"""
        # Simplified validation - in real implementation, call C++ chess engine
        try:
            from_file = ord(move_data['from'][0]) - ord('a')
            from_rank = 8 - int(move_data['from'][1])
            to_file = ord(move_data['to'][0]) - ord('a')
            to_rank = 8 - int(move_data['to'][1])
            
            # Basic bounds checking
            if not (0 <= from_file < 8 and 0 <= from_rank < 8 and 
                   0 <= to_file < 8 and 0 <= to_rank < 8):
                return False
            
            # Check if piece exists
            piece = board[from_rank][from_file]
            if piece is None:
                return False
            
            return True
        except:
            return False
    
    def execute_move(self, board, move_data):
        """Execute a move on the board"""
        from_file = ord(move_data['from'][0]) - ord('a')
        from_rank = 8 - int(move_data['from'][1])
        to_file = ord(move_data['to'][0]) - ord('a')
        to_rank = 8 - int(move_data['to'][1])
        
        # Move piece
        board[to_rank][to_file] = board[from_rank][from_file]
        board[from_rank][from_file] = None
    
    async def broadcast_move(self, game, move_record):
        """Broadcast move to both players"""
        move_message = {
            'type': 'move_made',
            'move': move_record,
            'board_state': game.board_state,
            'current_turn': game.current_turn.value
        }
        
        await game.white_player.websocket.send(json.dumps(move_message))
        await game.black_player.websocket.send(json.dumps(move_message))
    
    async def check_game_end(self, game):
        """Check if the game has ended"""
        # Simplified check - would integrate with C++ engine
        white_king = any('K' in row for row in game.board_state)
        black_king = any('k' in row for row in game.board_state)
        
        if not white_king:
            await self.end_game(game, 'black_wins')
        elif not black_king:
            await self.end_game(game, 'white_wins')
    
    async def end_game(self, game, result):
        """End the game"""
        game.status = GameStatus.FINISHED
        end_message = {
            'type': 'game_ended',
            'result': result,
            'move_history': game.move_history
        }
        
        await game.white_player.websocket.send(json.dumps(end_message))
        await game.black_player.websocket.send(json.dumps(end_message))
    
    async def send_error(self, websocket, message):
        """Send error message to client"""
        error_message = {
            'type': 'error',
            'message': message
        }
        await websocket.send(json.dumps(error_message))
    
    async def handle_client(self, websocket, path):
        """Handle WebSocket connection"""
        player_id = None
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    message_type = data.get('type')
                    
                    if message_type == 'register':
                        # Register new player
                        player_name = data.get('name', 'Anonymous')
                        player_id = await self.register_player(websocket, player_name)
                        
                        response = {
                            'type': 'registered',
                            'player_id': player_id,
                            'message': f'Welcome {player_name}! Looking for opponent...'
                        }
                        await websocket.send(json.dumps(response))
                        
                    elif message_type == 'move' and player_id:
                        # Handle move
                        game_id = data.get('game_id')
                        move_data = data.get('move')
                        if game_id and move_data:
                            await self.handle_move(game_id, player_id, move_data)
                            
                    elif message_type == 'ping':
                        # Keep-alive ping
                        pong_message = {'type': 'pong'}
                        await websocket.send(json.dumps(pong_message))
                        
                except json.JSONDecodeError:
                    await self.send_error(websocket, "Invalid JSON message")
                except Exception as e:
                    await self.send_error(websocket, f"Error processing message: {str(e)}")
                    
        except websockets.exceptions.ConnectionClosed:
            pass
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            # Clean up player
            if player_id and player_id in self.players:
                del self.players[player_id]
                self.waiting_players.discard(player_id)
    
    async def start_server(self):
        """Start the WebSocket server"""
        print(f"♔ ♕ ♖ ♗ ♘ ♙ CHESS WEBSOCKET SERVER STARTED ♟ ♞ ♝ ♜ ♛ ♚")
        print(f"🌐 WebSocket server running at: ws://{self.host}:{self.port}")
        print(f"🎮 Ready for real-time multiplayer chess games")
        print(f"🔄 Press Ctrl+C to stop the server")
        print("=" * 60)
        
        server = await websockets.serve(self.handle_client, self.host, self.port)
        await server.wait_closed()

def main():
    """Main function to run the WebSocket server"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Chess WebSocket Server for Multiplayer')
    parser.add_argument('-p', '--port', type=int, default=8765,
                       help='Port to run the WebSocket server on (default: 8765)')
    parser.add_argument('--host', default='localhost',
                       help='Host to bind to (default: localhost)')
    
    args = parser.parse_args()
    
    server = ChessWebSocketServer(host=args.host, port=args.port)
    
    try:
        asyncio.run(server.start_server())
    except KeyboardInterrupt:
        print("\n🛑 WebSocket server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")

if __name__ == "__main__":
    main()