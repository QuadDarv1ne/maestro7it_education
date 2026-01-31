#!/usr/bin/env python3
"""
Dedicated Network Chess Server
Professional multiplayer chess server with matchmaking and room system
"""

import asyncio
import websockets
import json
import uuid
import logging
from datetime import datetime
from typing import Dict, List, Set, Optional
from dataclasses import dataclass, asdict
from enum import Enum

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GameStatus(Enum):
    WAITING = "waiting"
    ACTIVE = "active"
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
    connected: bool = True
    rating: int = 1200
    games_played: int = 0

@dataclass
class ChessGame:
    id: str
    white_player: str
    black_player: str
    status: GameStatus = GameStatus.WAITING
    moves: List[str] = None
    current_turn: PlayerColor = PlayerColor.WHITE
    start_time: datetime = None
    end_time: Optional[datetime] = None
    winner: Optional[str] = None
    reason: Optional[str] = None
    
    def __post_init__(self):
        if self.moves is None:
            self.moves = []

class NetworkChessServer:
    def __init__(self, host='localhost', port=8766):
        self.host = host
        self.port = port
        self.players: Dict[str, Player] = {}
        self.games: Dict[str, ChessGame] = {}
        self.waiting_players: Set[str] = set()
        self.player_games: Dict[str, str] = {}  # player_id -> game_id
        self.game_lock = asyncio.Lock()
        
    async def start_server(self):
        """Start the network chess server"""
        logger.info(f"Starting Network Chess Server on {self.host}:{self.port}")
        
        server = await websockets.serve(
            self.handle_client,
            self.host,
            self.port,
            ping_interval=20,
            ping_timeout=10
        )
        
        logger.info("Network Chess Server is running and accepting connections")
        await server.wait_closed()
    
    async def handle_client(self, websocket, path):
        """Handle incoming WebSocket connections"""
        player_id = str(uuid.uuid4())
        player_name = f"Player_{player_id[:8]}"
        
        try:
            # Register new player
            player = Player(id=player_id, name=player_name, websocket=websocket)
            self.players[player_id] = player
            logger.info(f"Player {player_name} ({player_id}) connected")
            
            # Send welcome message
            await self.send_message(websocket, {
                'type': 'welcome',
                'player_id': player_id,
                'player_name': player_name,
                'server_time': datetime.now().isoformat()
            })
            
            # Add to waiting pool
            self.waiting_players.add(player_id)
            await self.update_lobby_status()
            
            # Try to match with another player
            await self.attempt_matchmaking(player_id)
            
            # Handle messages from client
            async for message in websocket:
                try:
                    data = json.loads(message)
                    await self.process_message(player_id, data)
                except json.JSONDecodeError:
                    await self.send_error(websocket, "Invalid JSON message")
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    await self.send_error(websocket, f"Processing error: {str(e)}")
                    
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Player {player_name} disconnected")
        except Exception as e:
            logger.error(f"Unexpected error with player {player_name}: {e}")
        finally:
            await self.handle_disconnect(player_id)
    
    async def process_message(self, player_id: str, data: dict):
        """Process incoming messages from clients"""
        message_type = data.get('type')
        
        if message_type == 'set_name':
            await self.set_player_name(player_id, data.get('name'))
        elif message_type == 'join_queue':
            await self.join_matchmaking_queue(player_id)
        elif message_type == 'leave_queue':
            await self.leave_matchmaking_queue(player_id)
        elif message_type == 'make_move':
            await self.handle_move(player_id, data)
        elif message_type == 'resign':
            await self.handle_resign(player_id)
        elif message_type == 'offer_draw':
            await self.handle_draw_offer(player_id, data)
        elif message_type == 'chat':
            await self.handle_chat(player_id, data)
        else:
            player = self.players.get(player_id)
            if player:
                await self.send_error(player.websocket, f"Unknown message type: {message_type}")
    
    async def set_player_name(self, player_id: str, name: str):
        """Set player's display name"""
        if not name or len(name) > 20:
            player = self.players.get(player_id)
            if player:
                await self.send_error(player.websocket, "Invalid name (1-20 characters)")
            return
            
        player = self.players.get(player_id)
        if player:
            old_name = player.name
            player.name = name
            logger.info(f"Player {old_name} renamed to {name}")
            
            # Notify in lobby if player is waiting
            if player_id in self.waiting_players:
                await self.broadcast_to_waiting({
                    'type': 'player_renamed',
                    'player_id': player_id,
                    'old_name': old_name,
                    'new_name': name
                })
    
    async def join_matchmaking_queue(self, player_id: str):
        """Add player to matchmaking queue"""
        if player_id not in self.players:
            return
            
        self.waiting_players.add(player_id)
        player = self.players[player_id]
        logger.info(f"Player {player.name} joined matchmaking queue")
        
        await self.send_message(player.websocket, {
            'type': 'queue_joined',
            'position': len(self.waiting_players)
        })
        
        await self.update_lobby_status()
        await self.attempt_matchmaking(player_id)
    
    async def leave_matchmaking_queue(self, player_id: str):
        """Remove player from matchmaking queue"""
        if player_id in self.waiting_players:
            self.waiting_players.remove(player_id)
            player = self.players.get(player_id)
            if player:
                logger.info(f"Player {player.name} left matchmaking queue")
                await self.send_message(player.websocket, {'type': 'queue_left'})
                await self.update_lobby_status()
    
    async def attempt_matchmaking(self, player_id: str):
        """Attempt to match players for a new game"""
        async with self.game_lock:
            if len(self.waiting_players) >= 2:
                # Get two players for matching
                player_ids = list(self.waiting_players)[:2]
                white_id, black_id = player_ids
                
                # Remove from waiting pool
                self.waiting_players.discard(white_id)
                self.waiting_players.discard(black_id)
                
                # Create new game
                game_id = str(uuid.uuid4())
                game = ChessGame(
                    id=game_id,
                    white_player=white_id,
                    black_player=black_id,
                    status=GameStatus.ACTIVE,
                    start_time=datetime.now()
                )
                
                self.games[game_id] = game
                self.player_games[white_id] = game_id
                self.player_games[black_id] = game_id
                
                # Notify players
                white_player = self.players[white_id]
                black_player = self.players[black_id]
                
                game_start_msg = {
                    'type': 'game_start',
                    'game_id': game_id,
                    'color': 'white',
                    'opponent': black_player.name,
                    'opponent_rating': black_player.rating
                }
                
                await self.send_message(white_player.websocket, game_start_msg)
                
                game_start_msg['color'] = 'black'
                game_start_msg['opponent'] = white_player.name
                game_start_msg['opponent_rating'] = white_player.rating
                
                await self.send_message(black_player.websocket, game_start_msg)
                
                logger.info(f"Match created: {white_player.name} (W) vs {black_player.name} (B) - Game {game_id}")
                
                # Update lobby status
                await self.update_lobby_status()
    
    async def handle_move(self, player_id: str, data: dict):
        """Handle move submission from player"""
        game_id = self.player_games.get(player_id)
        if not game_id:
            player = self.players.get(player_id)
            if player:
                await self.send_error(player.websocket, "Not in an active game")
            return
        
        game = self.games.get(game_id)
        if not game or game.status != GameStatus.ACTIVE:
            return
        
        # Validate it's player's turn
        player_color = self.get_player_color(player_id, game)
        if not player_color or player_color != game.current_turn:
            player = self.players.get(player_id)
            if player:
                await self.send_error(player.websocket, "Not your turn")
            return
        
        move = data.get('move')
        if not move:
            return
        
        # Add move to game
        game.moves.append(move)
        
        # Switch turns
        game.current_turn = PlayerColor.BLACK if game.current_turn == PlayerColor.WHITE else PlayerColor.WHITE
        
        # Notify both players
        opponent_id = game.black_player if player_id == game.white_player else game.white_player
        opponent = self.players.get(opponent_id)
        
        if opponent and opponent.connected:
            await self.send_message(opponent.websocket, {
                'type': 'move_made',
                'move': move,
                'by': player_id,
                'your_turn': True
            })
        
        player = self.players.get(player_id)
        if player and player.connected:
            await self.send_message(player.websocket, {
                'type': 'move_confirmed',
                'move': move,
                'your_turn': False
            })
        
        logger.info(f"Move {move} made in game {game_id} by {player.name if player else 'Unknown'}")
    
    async def handle_resign(self, player_id: str):
        """Handle player resignation"""
        game_id = self.player_games.get(player_id)
        if not game_id:
            return
        
        game = self.games.get(game_id)
        if not game or game.status != GameStatus.ACTIVE:
            return
        
        # Determine winner
        winner_id = game.black_player if player_id == game.white_player else game.white_player
        loser_id = player_id
        
        game.status = GameStatus.FINISHED
        game.winner = winner_id
        game.reason = "resignation"
        game.end_time = datetime.now()
        
        # Notify players
        winner = self.players.get(winner_id)
        loser = self.players.get(loser_id)
        
        if winner and winner.connected:
            await self.send_message(winner.websocket, {
                'type': 'game_won',
                'reason': 'opponent_resigned',
                'winner': winner_id
            })
        
        if loser and loser.connected:
            await self.send_message(loser.websocket, {
                'type': 'game_lost',
                'reason': 'resigned',
                'winner': winner_id
            })
        
        # Update ratings (simple Elo system)
        await self.update_ratings(winner_id, loser_id)
        
        logger.info(f"Game {game_id} ended by resignation - Winner: {winner.name if winner else 'Unknown'}")
    
    async def handle_draw_offer(self, player_id: str, data: dict):
        """Handle draw offers and acceptance"""
        game_id = self.player_games.get(player_id)
        if not game_id:
            return
        
        game = self.games.get(game_id)
        if not game or game.status != GameStatus.ACTIVE:
            return
        
        offer = data.get('offer', False)
        accept = data.get('accept', False)
        
        opponent_id = game.black_player if player_id == game.white_player else game.white_player
        
        if offer:
            opponent = self.players.get(opponent_id)
            if opponent and opponent.connected:
                await self.send_message(opponent.websocket, {
                    'type': 'draw_offered',
                    'by': player_id
                })
        elif accept:
            # Draw accepted
            game.status = GameStatus.FINISHED
            game.reason = "draw_agreed"
            game.end_time = datetime.now()
            
            # Notify both players
            for pid in [player_id, opponent_id]:
                player = self.players.get(pid)
                if player and player.connected:
                    await self.send_message(player.websocket, {
                        'type': 'game_drawn',
                        'reason': 'mutual_agreement'
                    })
            
            logger.info(f"Game {game_id} drawn by mutual agreement")
    
    async def handle_chat(self, player_id: str, data: dict):
        """Handle chat messages"""
        game_id = self.player_games.get(player_id)
        if not game_id:
            return
        
        game = self.games.get(game_id)
        if not game:
            return
        
        message = data.get('message', '')
        if not message:
            return
        
        # Broadcast to both players
        sender = self.players.get(player_id)
        opponent_id = game.black_player if player_id == game.white_player else game.white_player
        opponent = self.players.get(opponent_id)
        
        chat_msg = {
            'type': 'chat_message',
            'sender_id': player_id,
            'sender_name': sender.name if sender else 'Unknown',
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        
        if sender and sender.connected:
            await self.send_message(sender.websocket, chat_msg)
        
        if opponent and opponent.connected:
            await self.send_message(opponent.websocket, chat_msg)
    
    async def handle_disconnect(self, player_id: str):
        """Handle player disconnection"""
        player = self.players.get(player_id)
        if player:
            player.connected = False
            logger.info(f"Player {player.name} disconnected")
        
        # Remove from waiting queue
        self.waiting_players.discard(player_id)
        
        # Handle game abandonment
        game_id = self.player_games.get(player_id)
        if game_id:
            game = self.games.get(game_id)
            if game and game.status == GameStatus.ACTIVE:
                # Mark game as abandoned
                game.status = GameStatus.ABANDONED
                game.end_time = datetime.now()
                game.reason = "player_disconnected"
                
                # Award win to opponent
                opponent_id = game.black_player if player_id == game.white_player else game.white_player
                game.winner = opponent_id
                
                opponent = self.players.get(opponent_id)
                if opponent and opponent.connected:
                    await self.send_message(opponent.websocket, {
                        'type': 'game_won',
                        'reason': 'opponent_disconnected',
                        'winner': opponent_id
                    })
                
                logger.info(f"Game {game_id} abandoned due to disconnection")
        
        # Clean up player mappings
        if player_id in self.player_games:
            del self.player_games[player_id]
        
        await self.update_lobby_status()
    
    def get_player_color(self, player_id: str, game: ChessGame) -> Optional[PlayerColor]:
        """Get player's color in a game"""
        if player_id == game.white_player:
            return PlayerColor.WHITE
        elif player_id == game.black_player:
            return PlayerColor.BLACK
        return None
    
    async def update_ratings(self, winner_id: str, loser_id: str):
        """Simple Elo rating update"""
        winner = self.players.get(winner_id)
        loser = self.players.get(loser_id)
        
        if not winner or not loser:
            return
        
        # Simplified Elo calculation
        k_factor = 32
        rating_diff = loser.rating - winner.rating
        expected_winner = 1 / (1 + 10 ** (rating_diff / 400))
        
        winner.rating = int(winner.rating + k_factor * (1 - expected_winner))
        loser.rating = int(loser.rating + k_factor * (0 - (1 - expected_winner)))
        
        winner.games_played += 1
        loser.games_played += 1
    
    async def update_lobby_status(self):
        """Send updated lobby status to all waiting players"""
        lobby_info = {
            'type': 'lobby_update',
            'players_waiting': len(self.waiting_players),
            'active_games': len([g for g in self.games.values() if g.status == GameStatus.ACTIVE]),
            'players_online': len([p for p in self.players.values() if p.connected])
        }
        
        await self.broadcast_to_waiting(lobby_info)
    
    async def broadcast_to_waiting(self, message: dict):
        """Broadcast message to all waiting players"""
        for player_id in list(self.waiting_players):
            player = self.players.get(player_id)
            if player and player.connected:
                try:
                    await self.send_message(player.websocket, message)
                except:
                    # Remove disconnected players
                    self.waiting_players.discard(player_id)
    
    async def send_message(self, websocket, message: dict):
        """Send JSON message to websocket"""
        try:
            await websocket.send(json.dumps(message, ensure_ascii=False))
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
    
    async def send_error(self, websocket, error_message: str):
        """Send error message to client"""
        await self.send_message(websocket, {
            'type': 'error',
            'message': error_message
        })

async def main():
    """Main server entry point"""
    server = NetworkChessServer(host='localhost', port=8766)
    await server.start_server()

if __name__ == "__main__":
    asyncio.run(main())