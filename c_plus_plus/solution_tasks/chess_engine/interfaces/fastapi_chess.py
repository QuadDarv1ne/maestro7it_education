#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FastAPI Шахматное веб-приложение
Современный, высокопроизводительный шахматный веб-интерфейс с real-time возможностями
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Optional, Tuple
import asyncio
import json
import uuid
from datetime import datetime, timedelta
import logging
import time
from functools import wraps
from collections import defaultdict

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Импорт шахматных компонентов
from core.chess_engine_wrapper import ChessEngineWrapper
from core.optimized_move_generator import BitboardMoveGenerator
from core.enhanced_chess_ai import EnhancedChessAI
from src.pgn_saver import PGNSaver, GameRecorder
from src.san_parser import SANParser
from src.endgame_tablebase import SimplifiedEndgameTablebase

app = FastAPI(
    title="Chess Engine API",
    description="High-performance chess engine with FastAPI backend",
    version="2.0.0"
)

# Rate limiting
class RateLimiter:
    """Простой rate limiter для защиты от злоупотреблений"""
    def __init__(self, requests: int = 100, window: int = 60):
        self.requests = requests
        self.window = window
        self.clients = defaultdict(list)
    
    def is_allowed(self, client_id: str) -> bool:
        """Проверка, разрешен ли запрос от клиента"""
        now = time.time()
        # Очистка старых запросов
        self.clients[client_id] = [
            req_time for req_time in self.clients[client_id]
            if now - req_time < self.window
        ]
        
        if len(self.clients[client_id]) >= self.requests:
            return False
        
        self.clients[client_id].append(now)
        return True

rate_limiter = RateLimiter(requests=100, window=60)

# Middleware для логирования и rate limiting
@app.middleware("http")
async def add_process_time_and_rate_limit(request: Request, call_next):
    """Middleware для замера времени обработки и rate limiting"""
    start_time = time.time()
    
    # Rate limiting по IP
    client_ip = request.client.host if request.client else "unknown"
    if not rate_limiter.is_allowed(client_ip):
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests. Please try again later."}
        )
    
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")
    return response

# Добавление CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Добавление GZip сжатия для улучшения производительности
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Подключение статических файлов
app.mount("/static", StaticFiles(directory="web"), name="static")

# Управление играми
class GameManager:
    def __init__(self):
        self.games: Dict[str, dict] = {}
        self.connections: Dict[str, List[WebSocket]] = {}
        self.chat_history: Dict[str, List[Dict]] = defaultdict(list)  # История чата по играм
        self.matchmaking_queue: List[Dict] = []  # Очередь на поиск игры
        self.lobbies: Dict[str, Dict] = {}  # Игровые лобби для мультиплеера
        self.pgn_saver = PGNSaver()  # PGN сохранение
        self.game_recorders: Dict[str, GameRecorder] = {}  # Рекордеры для каждой игры
    
    def create_game(self, player_name: str = "Anonymous", game_mode: str = "ai", time_control: int = 0) -> str:
        game_id = str(uuid.uuid4())
        # Конвертация времени из минут в секунды
        time_per_player = time_control * 60 if time_control > 0 else 0
        
        # Инициализация PGN рекордера
        recorder = GameRecorder()
        recorder.start_recording(white_player=player_name, black_player="AI" if game_mode == "ai" else "Opponent")
        self.game_recorders[game_id] = recorder
        
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
            'winner': None,
            'time_control': time_control,  # Время в минутах
            'white_time': time_per_player,  # Оставшееся время белых в секундах
            'black_time': time_per_player,  # Оставшееся время черных в секундах
            'move_start_time': time.time() if time_control > 0 else None  # Время начала хода
        }
        self.connections[game_id] = []
        logger.info(f"Created game {game_id} for player {player_name} with time control {time_control}min")
        return game_id
    
    def get_game(self, game_id: str) -> Optional[dict]:
        return self.games.get(game_id)
    
    def delete_game(self, game_id: str):
        if game_id in self.games:
            del self.games[game_id]
        if game_id in self.connections:
            del self.connections[game_id]
        if game_id in self.chat_history:
            del self.chat_history[game_id]
        if game_id in self.game_recorders:
            del self.game_recorders[game_id]
        logger.info(f"Deleted game {game_id}")
    
    def add_chat_message(self, game_id: str, player_name: str, message: str):
        """Добавление сообщения в чат"""
        chat_message = {
            'player': player_name,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        self.chat_history[game_id].append(chat_message)
        
        # Ограничение истории чата (100 сообщений)
        if len(self.chat_history[game_id]) > 100:
            self.chat_history[game_id] = self.chat_history[game_id][-100:]
        
        return chat_message
    
    def get_chat_history(self, game_id: str, limit: int = 50) -> List[Dict]:
        """Получение истории чата"""
        messages = self.chat_history.get(game_id, [])
        return messages[-limit:] if limit > 0 else messages
    
    def add_to_matchmaking(self, player_name: str, rating: int = 1000, time_control: int = 0) -> str:
        """Добавление игрока в очередь поиска игры"""
        player_id = str(uuid.uuid4())
        player_data = {
            'player_id': player_id,
            'player_name': player_name,
            'rating': rating,
            'time_control': time_control,
            'joined_at': datetime.now()
        }
        self.matchmaking_queue.append(player_data)
        logger.info(f"Player {player_name} joined matchmaking queue")
        return player_id
    
    def remove_from_matchmaking(self, player_id: str):
        """Удаление игрока из очереди"""
        self.matchmaking_queue = [p for p in self.matchmaking_queue if p['player_id'] != player_id]
    
    def find_match(self, player_id: str) -> Optional[Tuple[str, str]]:
        """Поиск подходящего соперника"""
        player = next((p for p in self.matchmaking_queue if p['player_id'] == player_id), None)
        if not player:
            return None
        
        # Поиск игрока с близким рейтингом
        for opponent in self.matchmaking_queue:
            if opponent['player_id'] == player_id:
                continue
            
            # Проверка совместимости рейтингов (±200)
            rating_diff = abs(player['rating'] - opponent['rating'])
            if rating_diff <= 200 and player['time_control'] == opponent['time_control']:
                # Создание игры
                game_id = self.create_multiplayer_game(
                    player['player_name'],
                    opponent['player_name'],
                    player['time_control']
                )
                
                # Удаление из очереди
                self.remove_from_matchmaking(player_id)
                self.remove_from_matchmaking(opponent['player_id'])
                
                return (game_id, opponent['player_id'])
        
        return None
    
    def create_multiplayer_game(self, white_player: str, black_player: str, time_control: int = 0) -> str:
        """Создание мультиплеерной игры"""
        game_id = str(uuid.uuid4())
        time_per_player = time_control * 60 if time_control > 0 else 0
        
        self.games[game_id] = {
            'id': game_id,
            'white_player': white_player,
            'black_player': black_player,
            'game_mode': 'multiplayer',
            'engine': ChessEngineWrapper(),
            'ai': None,
            'move_generator': BitboardMoveGenerator(),
            'created_at': datetime.now(),
            'last_move_time': datetime.now(),
            'move_history': [],
            'current_player': True,
            'game_status': 'active',
            'winner': None,
            'time_control': time_control,
            'white_time': time_per_player,
            'black_time': time_per_player,
            'move_start_time': time.time() if time_control > 0 else None
        }
        self.connections[game_id] = []
        logger.info(f"Created multiplayer game {game_id}: {white_player} vs {black_player}")
        return game_id
    
    def create_lobby(self, host_name: str, lobby_name: str, time_control: int = 0, is_private: bool = False) -> str:
        """Создание игрового лобби"""
        lobby_id = str(uuid.uuid4())
        self.lobbies[lobby_id] = {
            'lobby_id': lobby_id,
            'lobby_name': lobby_name,
            'host': host_name,
            'guest': None,
            'time_control': time_control,
            'is_private': is_private,
            'created_at': datetime.now(),
            'status': 'waiting'  # waiting, ready, playing
        }
        logger.info(f"Created lobby {lobby_id} by {host_name}")
        return lobby_id
    
    def join_lobby(self, lobby_id: str, player_name: str) -> bool:
        """Присоединение к лобби"""
        if lobby_id not in self.lobbies:
            return False
        
        lobby = self.lobbies[lobby_id]
        if lobby['guest'] is not None:
            return False
        
        lobby['guest'] = player_name
        lobby['status'] = 'ready'
        logger.info(f"Player {player_name} joined lobby {lobby_id}")
        return True
    
    def start_lobby_game(self, lobby_id: str) -> Optional[str]:
        """Запуск игры из лобби"""
        if lobby_id not in self.lobbies:
            return None
        
        lobby = self.lobbies[lobby_id]
        if lobby['status'] != 'ready':
            return None
        
        game_id = self.create_multiplayer_game(
            lobby['host'],
            lobby['guest'],
            lobby['time_control']
        )
        
        lobby['status'] = 'playing'
        lobby['game_id'] = game_id
        return game_id
    
    def get_public_lobbies(self) -> List[Dict]:
        """Получение списка публичных лобби"""
        return [
            {
                'lobby_id': lid,
                'lobby_name': lobby['lobby_name'],
                'host': lobby['host'],
                'status': lobby['status'],
                'time_control': lobby['time_control']
            }
            for lid, lobby in self.lobbies.items()
            if not lobby['is_private'] and lobby['status'] == 'waiting'
        ]

game_manager = GameManager()

# Кэш для AI ходов
class MoveCache:
    """Кэш для хранения вычисленных AI ходов"""
    def __init__(self, max_size: int = 1000, ttl: int = 300):
        self.cache = {}
        self.max_size = max_size
        self.ttl = ttl
    
    def get(self, key: str) -> Optional[Dict]:
        """Получение хода из кэша"""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return data
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value: Dict):
        """Сохранение хода в кэш"""
        # Очистка старых записей
        if len(self.cache) >= self.max_size:
            oldest = min(self.cache.items(), key=lambda x: x[1][1])
            del self.cache[oldest[0]]
        
        self.cache[key] = (value, time.time())
    
    def clear(self):
        """Очистка всего кэша"""
        self.cache.clear()

move_cache = MoveCache()

# Статистика игроков
class PlayerStats:
    """Хранение и управление статистикой игроков"""
    def __init__(self):
        self.stats: Dict[str, Dict] = defaultdict(lambda: {
            'games_played': 0,
            'wins': 0,
            'losses': 0,
            'draws': 0,
            'total_moves': 0,
            'avg_game_time': 0,
            'longest_game': 0,
            'shortest_game': float('inf'),
            'favorite_opening': None,
            'win_rate': 0.0
        })
    
    def update_stats(self, player_name: str, game_data: Dict):
        """Обновление статистики после игры"""
        stats = self.stats[player_name]
        stats['games_played'] += 1
        
        if game_data.get('winner') == player_name:
            stats['wins'] += 1
        elif game_data.get('winner') and game_data.get('winner') != player_name:
            stats['losses'] += 1
        else:
            stats['draws'] += 1
        
        moves = len(game_data.get('move_history', []))
        stats['total_moves'] += moves
        
        game_duration = (game_data.get('ended_at', datetime.now()) - 
                        game_data.get('created_at', datetime.now())).total_seconds()
        
        stats['longest_game'] = max(stats['longest_game'], game_duration)
        if stats['shortest_game'] == float('inf'):
            stats['shortest_game'] = game_duration
        else:
            stats['shortest_game'] = min(stats['shortest_game'], game_duration)
        
        # Расчет среднего времени игры
        stats['avg_game_time'] = (
            stats['avg_game_time'] * (stats['games_played'] - 1) + game_duration
        ) / stats['games_played']
        
        # Расчет процента побед
        if stats['games_played'] > 0:
            stats['win_rate'] = (stats['wins'] / stats['games_played']) * 100
    
    def get_stats(self, player_name: str) -> Dict:
        """Получение статистики игрока"""
        return dict(self.stats[player_name])
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Получение таблицы лидеров"""
        leaderboard = []
        for player, stats in self.stats.items():
            leaderboard.append({
                'player': player,
                'wins': stats['wins'],
                'games': stats['games_played'],
                'win_rate': stats['win_rate']
            })
        
        return sorted(leaderboard, key=lambda x: x['win_rate'], reverse=True)[:limit]

player_stats = PlayerStats()

# История игр
class GameHistory:
    """Хранение истории завершенных игр"""
    def __init__(self, max_games: int = 100):
        self.games: List[Dict] = []
        self.max_games = max_games
    
    def add_game(self, game_data: Dict):
        """Добавление игры в историю"""
        game_record = {
            'game_id': game_data['id'],
            'player_name': game_data['player_name'],
            'game_mode': game_data['game_mode'],
            'winner': game_data.get('winner'),
            'game_status': game_data['game_status'],
            'moves': len(game_data['move_history']),
            'duration': (game_data.get('ended_at', datetime.now()) - 
                        game_data['created_at']).total_seconds(),
            'time_control': game_data['time_control'],
            'created_at': game_data['created_at'].isoformat(),
            'ended_at': game_data.get('ended_at', datetime.now()).isoformat(),
            'move_history': game_data['move_history']
        }
        
        self.games.insert(0, game_record)  # Новые игры вверху
        
        # Ограничение размера истории
        if len(self.games) > self.max_games:
            self.games = self.games[:self.max_games]
    
    def get_recent_games(self, limit: int = 10) -> List[Dict]:
        """Получение последних игр"""
        return self.games[:limit]
    
    def get_player_games(self, player_name: str, limit: int = 10) -> List[Dict]:
        """Получение игр конкретного игрока"""
        player_games = [g for g in self.games if g['player_name'] == player_name]
        return player_games[:limit]
    
    def export_to_pgn(self, game_id: str) -> str:
        """Экспорт игры в формат PGN"""
        game = next((g for g in self.games if g['game_id'] == game_id), None)
        if not game:
            return ""
        
        pgn = f"[Event \"FastAPI Chess Game\"]\n"
        pgn += f"[Site \"Chess Master\"]\n"
        pgn += f"[Date \"{game['created_at'][:10]}\"]\n"
        pgn += f"[White \"{game['player_name']}\"]\n"
        pgn += f"[Black \"{'AI' if game['game_mode'] == 'ai' else 'Human'}\"]\n"
        pgn += f"[Result \"{self._get_result(game)}\"]\n"
        pgn += f"[TimeControl \"{game['time_control'] * 60 if game['time_control'] > 0 else '-'}\"]\n\n"
        
        # Добавление ходов
        moves_text = ""
        for i, move in enumerate(game['move_history']):
            if i % 2 == 0:
                moves_text += f"{i//2 + 1}. "
            moves_text += f"{move.get('notation', '')} "
        
        pgn += moves_text + self._get_result(game)
        return pgn
    
    def _get_result(self, game: Dict) -> str:
        """Получение результата игры в формате PGN"""
        if game['winner'] == game['player_name']:
            return "1-0"
        elif game['winner']:
            return "0-1"
        else:
            return "1/2-1/2"

game_history = GameHistory()

# Анализ партий
class GameAnalyzer:
    """Анализ завершенных партий"""
    def __init__(self):
        self.ai = EnhancedChessAI(search_depth=5)  # Более глубокий поиск для анализа
    
    def analyze_game(self, game_data: Dict) -> Dict:
        """Полный анализ партии"""
        moves = game_data['move_history']
        engine = ChessEngineWrapper()
        
        analysis = {
            'total_moves': len(moves),
            'blunders': [],  # Грубые ошибки (eval drop > 2)
            'mistakes': [],  # Ошибки (eval drop > 1)
            'inaccuracies': [],  # Неточности (eval drop > 0.5)
            'best_moves': [],  # Лучшие ходы в партии
            'accuracy': {'white': 0.0, 'black': 0.0},
            'avg_eval': 0.0,
            'position_analysis': []
        }
        
        prev_eval = 0.0
        eval_sum = 0.0
        white_accurate = 0
        black_accurate = 0
        white_total = 0
        black_total = 0
        
        # Анализ каждой позиции
        for i, move in enumerate(moves):
            is_white = i % 2 == 0
            
            # Получение лучшего хода от AI
            board = engine.get_board()
            best_move = self.ai.get_best_move(board, is_white)
            
            # Оценка позиции
            current_eval = self.ai.evaluate_position(board, is_white)
            eval_change = current_eval - prev_eval if not is_white else prev_eval - current_eval
            
            # Классификация хода
            move_quality = 'excellent'
            if abs(eval_change) < 0.2:
                if is_white:
                    white_accurate += 1
                else:
                    black_accurate += 1
            elif eval_change < -0.5:
                move_quality = 'inaccuracy'
                analysis['inaccuracies'].append({
                    'move_num': i + 1,
                    'player': 'White' if is_white else 'Black',
                    'move': move.get('notation', ''),
                    'eval_loss': round(abs(eval_change), 2)
                })
            elif eval_change < -1.0:
                move_quality = 'mistake'
                analysis['mistakes'].append({
                    'move_num': i + 1,
                    'player': 'White' if is_white else 'Black',
                    'move': move.get('notation', ''),
                    'eval_loss': round(abs(eval_change), 2),
                    'best_move': best_move
                })
            elif eval_change < -2.0:
                move_quality = 'blunder'
                analysis['blunders'].append({
                    'move_num': i + 1,
                    'player': 'White' if is_white else 'Black',
                    'move': move.get('notation', ''),
                    'eval_loss': round(abs(eval_change), 2),
                    'best_move': best_move
                })
            
            # Лучшие ходы
            if eval_change > 1.5:
                analysis['best_moves'].append({
                    'move_num': i + 1,
                    'player': 'White' if is_white else 'Black',
                    'move': move.get('notation', ''),
                    'eval_gain': round(eval_change, 2)
                })
            
            analysis['position_analysis'].append({
                'move_num': i + 1,
                'move': move.get('notation', ''),
                'evaluation': round(current_eval, 2),
                'quality': move_quality,
                'best_alternative': best_move if move_quality != 'excellent' else None
            })
            
            # Выполнение хода
            if 'from' in move and 'to' in move:
                engine.make_move(move['from'], move['to'])
            
            prev_eval = current_eval
            eval_sum += current_eval
            
            if is_white:
                white_total += 1
            else:
                black_total += 1
        
        # Расчет точности
        analysis['accuracy']['white'] = round((white_accurate / white_total * 100) if white_total > 0 else 0, 1)
        analysis['accuracy']['black'] = round((black_accurate / black_total * 100) if black_total > 0 else 0, 1)
        analysis['avg_eval'] = round(eval_sum / len(moves) if moves else 0, 2)
        
        return analysis
    
    def get_position_insights(self, board_state: List[List[str]], is_white: bool) -> Dict:
        """Получение подсказок для текущей позиции"""
        best_move = self.ai.get_best_move(board_state, is_white)
        evaluation = self.ai.evaluate_position(board_state, is_white)
        
        # Определение рекомендаций
        insights = {
            'best_move': best_move,
            'evaluation': round(evaluation, 2),
            'recommendation': self._get_recommendation(evaluation, is_white)
        }
        
        return insights
    
    def _get_recommendation(self, eval_score: float, is_white: bool) -> str:
        """Получение рекомендации на основе оценки"""
        if eval_score > 3:
            return "You have a winning advantage! Look for forcing moves."
        elif eval_score > 1:
            return "You have a clear advantage. Maintain pressure!"
        elif eval_score > 0.5:
            return "Slightly better position. Play carefully."
        elif eval_score > -0.5:
            return "Position is equal. Look for tactical opportunities."
        elif eval_score > -1:
            return "Slightly worse position. Defend actively."
        elif eval_score > -3:
            return "You are under pressure. Look for counterplay."
        else:
            return "Critical position! Focus on defense and tactics."

game_analyzer = GameAnalyzer()

# Система рейтингов ELO
class EloRatingSystem:
    """Система расчета рейтингов ELO для игроков"""
    def __init__(self, k_factor: int = 32, default_rating: int = 1200):
        self.k_factor = k_factor  # Коэффициент изменения рейтинга
        self.default_rating = default_rating  # Начальный рейтинг
        self.ratings: Dict[str, int] = defaultdict(lambda: default_rating)
        self.rating_history: Dict[str, List[Dict]] = defaultdict(list)
    
    def get_rating(self, player_name: str) -> int:
        """Получение текущего рейтинга игрока"""
        return self.ratings[player_name]
    
    def calculate_expected_score(self, rating_a: int, rating_b: int) -> float:
        """Расчет ожидаемого результата по формуле ELO"""
        return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))
    
    def update_ratings(self, player_name: str, opponent_rating: int, 
                       actual_score: float, game_id: str = None) -> Dict:
        """Обновление рейтинга после игры
        
        Args:
            player_name: Имя игрока
            opponent_rating: Рейтинг противника
            actual_score: Фактический результат (1.0 = победа, 0.5 = ничья, 0.0 = поражение)
            game_id: ID игры для истории
        
        Returns:
            Словарь с информацией об изменении рейтинга
        """
        current_rating = self.ratings[player_name]
        expected_score = self.calculate_expected_score(current_rating, opponent_rating)
        
        # Расчет нового рейтинга
        rating_change = round(self.k_factor * (actual_score - expected_score))
        new_rating = current_rating + rating_change
        
        # Ограничение минимального рейтинга
        new_rating = max(100, new_rating)
        
        # Сохранение истории
        history_entry = {
            'timestamp': datetime.now().isoformat(),
            'old_rating': current_rating,
            'new_rating': new_rating,
            'change': rating_change,
            'opponent_rating': opponent_rating,
            'actual_score': actual_score,
            'game_id': game_id
        }
        self.rating_history[player_name].append(history_entry)
        
        # Обновление рейтинга
        self.ratings[player_name] = new_rating
        
        return {
            'player': player_name,
            'old_rating': current_rating,
            'new_rating': new_rating,
            'change': rating_change,
            'expected_score': round(expected_score, 3)
        }
    
    def get_rating_history(self, player_name: str, limit: int = 10) -> List[Dict]:
        """Получение истории изменений рейтинга"""
        history = self.rating_history[player_name]
        return history[-limit:] if limit > 0 else history
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Получение таблицы лидеров по рейтингу"""
        leaderboard = [
            {'player': name, 'rating': rating, 'games': len(self.rating_history[name])}
            for name, rating in self.ratings.items()
        ]
        return sorted(leaderboard, key=lambda x: x['rating'], reverse=True)[:limit]
    
    def get_rank_title(self, rating: int) -> str:
        """Получение звания на основе рейтинга"""
        if rating >= 2400:
            return "Grandmaster"
        elif rating >= 2200:
            return "Master"
        elif rating >= 2000:
            return "Expert"
        elif rating >= 1800:
            return "Class A"
        elif rating >= 1600:
            return "Class B"
        elif rating >= 1400:
            return "Class C"
        elif rating >= 1200:
            return "Class D"
        else:
            return "Novice"

elo_system = EloRatingSystem()

# База данных дебютов
class OpeningBook:
    """Определение шахматных дебютов по последовательности ходов"""
    def __init__(self):
        # Словарь дебютов: ключ - последовательность ходов, значение - название
        self.openings = {
            # Открытые дебюты (1.e4 e5)
            "e2-e4 e7-e5": "King's Pawn Opening",
            "e2-e4 e7-e5 g1-f3": "King's Knight Opening",
            "e2-e4 e7-e5 g1-f3 b8-c6": "King's Knight Opening",
            "e2-e4 e7-e5 g1-f3 b8-c6 f1-b5": "Ruy Lopez (Spanish Opening)",
            "e2-e4 e7-e5 g1-f3 b8-c6 f1-c4": "Italian Game",
            "e2-e4 e7-e5 g1-f3 b8-c6 f1-c4 f8-c5": "Giuoco Piano",
            "e2-e4 e7-e5 g1-f3 b8-c6 d2-d4": "Scotch Game",
            "e2-e4 e7-e5 f2-f4": "King's Gambit",
            "e2-e4 e7-e5 b1-c3 g8-f6": "Vienna Game",
            
            # Полуоткрытые дебюты (1.e4 не e5)
            "e2-e4 c7-c5": "Sicilian Defense",
            "e2-e4 c7-c5 g1-f3": "Sicilian Defense: Open",
            "e2-e4 c7-c5 g1-f3 d7-d6": "Sicilian Defense: Najdorf Preparation",
            "e2-e4 c7-c5 g1-f3 b8-c6": "Sicilian Defense: Old Sicilian",
            "e2-e4 e7-e6": "French Defense",
            "e2-e4 e7-e6 d2-d4 d7-d5": "French Defense: Main Line",
            "e2-e4 c7-c6": "Caro-Kann Defense",
            "e2-e4 c7-c6 d2-d4 d7-d5": "Caro-Kann Defense: Main Line",
            "e2-e4 d7-d5": "Scandinavian Defense",
            "e2-e4 g8-f6": "Alekhine's Defense",
            "e2-e4 d7-d6": "Pirc Defense",
            
            # Закрытые дебюты (1.d4 d5)
            "d2-d4 d7-d5": "Queen's Pawn Game",
            "d2-d4 d7-d5 c2-c4": "Queen's Gambit",
            "d2-d4 d7-d5 c2-c4 e7-e6": "Queen's Gambit Declined",
            "d2-d4 d7-d5 c2-c4 d5-c4": "Queen's Gambit Accepted",
            "d2-d4 d7-d5 c2-c4 c7-c6": "Slav Defense",
            "d2-d4 d7-d5 g1-f3 g8-f6": "Queen's Pawn Game",
            
            # Индийские дебюты (1.d4 не d5)
            "d2-d4 g8-f6": "Indian Defense",
            "d2-d4 g8-f6 c2-c4": "Indian Game",
            "d2-d4 g8-f6 c2-c4 e7-e6": "Indian Game: Nimzo-Indian Preparation",
            "d2-d4 g8-f6 c2-c4 g7-g6": "King's Indian Defense",
            "d2-d4 g8-f6 c2-c4 e7-e6 b1-c3 f8-b4": "Nimzo-Indian Defense",
            "d2-d4 g8-f6 c2-c4 c7-c5": "Benoni Defense",
            "d2-d4 g8-f6 g1-f3 e7-e6": "Indian Game",
            
            # Фланговые дебюты
            "c2-c4": "English Opening",
            "c2-c4 e7-e5": "English Opening: King's English",
            "c2-c4 g8-f6": "English Opening: Anglo-Indian Defense",
            "c2-c4 c7-c5": "English Opening: Symmetrical",
            "g1-f3": "Zukertort Opening (Reti)",
            "g1-f3 d7-d5": "Zukertort Opening",
            "g1-f3 g8-f6": "Zukertort Opening: King's Indian Attack",
            "b2-b3": "Nimzowitsch-Larsen Attack",
            "f2-f4": "Bird's Opening",
            
            # Редкие дебюты
            "e2-e3": "Van't Kruijs Opening",
            "b1-c3": "Dunst Opening",
            "a2-a3": "Anderssen's Opening",
            "h2-h3": "Clemenz Opening",
            "g2-g4": "Grob's Attack",
        }
    
    def identify_opening(self, move_history: List[Dict]) -> Dict:
        """Определение дебюта по истории ходов
        
        Args:
            move_history: История ходов игры
        
        Returns:
            Словарь с информацией о дебюте
        """
        if not move_history:
            return {
                'name': 'Starting Position',
                'moves_count': 0,
                'category': 'none'
            }
        
        # Формирование последовательности ходов
        move_sequence = []
        for move in move_history[:10]:  # Проверяем первые 10 ходов
            if 'notation' in move:
                move_sequence.append(move['notation'])
        
        # Поиск самого длинного совпадения
        best_match = None
        max_moves = 0
        
        for i in range(len(move_sequence), 0, -1):
            sequence = ' '.join(move_sequence[:i])
            if sequence in self.openings:
                best_match = self.openings[sequence]
                max_moves = i
                break
        
        if best_match:
            # Определение категории дебюта
            category = self._categorize_opening(move_sequence[0] if move_sequence else '')
            
            return {
                'name': best_match,
                'moves_count': max_moves,
                'category': category,
                'sequence': ' '.join(move_sequence[:max_moves])
            }
        else:
            return {
                'name': 'Unknown Opening',
                'moves_count': len(move_sequence),
                'category': 'custom',
                'sequence': ' '.join(move_sequence[:3]) if len(move_sequence) >= 3 else ''
            }
    
    def _categorize_opening(self, first_move: str) -> str:
        """Категоризация дебюта по первому ходу"""
        if first_move.startswith('e2-e4'):
            return 'open'
        elif first_move.startswith('d2-d4'):
            return 'closed'
        elif first_move in ['c2-c4', 'g1-f3', 'g2-g3', 'b2-b3']:
            return 'flank'
        else:
            return 'other'
    
    def get_opening_stats(self, player_name: str, games: List[Dict]) -> Dict:
        """Статистика использования дебютов игроком"""
        opening_usage = defaultdict(int)
        opening_results = defaultdict(lambda: {'wins': 0, 'total': 0})
        
        for game in games:
            if game.get('player_name') == player_name:
                opening_info = self.identify_opening(game.get('move_history', []))
                opening_name = opening_info['name']
                
                opening_usage[opening_name] += 1
                opening_results[opening_name]['total'] += 1
                
                if game.get('winner') == player_name:
                    opening_results[opening_name]['wins'] += 1
        
        # Формирование статистики
        stats = []
        for opening, count in sorted(opening_usage.items(), key=lambda x: x[1], reverse=True)[:5]:
            wins = opening_results[opening]['wins']
            total = opening_results[opening]['total']
            win_rate = (wins / total * 100) if total > 0 else 0
            
            stats.append({
                'opening': opening,
                'games': count,
                'win_rate': round(win_rate, 1)
            })
        
        return {
            'most_played': stats,
            'total_unique_openings': len(opening_usage)
        }

opening_book = OpeningBook()
san_parser = SANParser()  # SAN notation parser
endgame_tablebase = SimplifiedEndgameTablebase()  # Endgame tablebase

# Расширенная система статистики игрока
class PlayerProfile:
    """Расширенный профиль игрока с детальной статистикой"""
    def __init__(self, player_name: str):
        self.player_name = player_name
        self.created_at = datetime.now()
        
        # Основная статистика
        self.games_played = 0
        self.wins = 0
        self.losses = 0
        self.draws = 0
        
        # Статистика по цвету
        self.white_stats = {'games': 0, 'wins': 0, 'losses': 0, 'draws': 0}
        self.black_stats = {'games': 0, 'wins': 0, 'losses': 0, 'draws': 0}
        
        # Статистика по режимам
        self.mode_stats = defaultdict(lambda: {'games': 0, 'wins': 0})
        
        # Временная статистика
        self.total_time_played = 0  # в секундах
        self.average_game_time = 0
        self.shortest_game = float('inf')
        self.longest_game = 0
        
        # Статистика ходов
        self.total_moves = 0
        self.average_moves_per_game = 0
        
        # Дебютная статистика
        self.opening_stats = defaultdict(lambda: {'games': 0, 'wins': 0, 'losses': 0, 'draws': 0})
        self.favorite_opening = None
        
        # Достижения
        self.achievements = []
        self.win_streak = 0
        self.best_win_streak = 0
        self.loss_streak = 0
        
        # Последняя активность
        self.last_game_at = None
        self.last_win_at = None
    
    def update_from_game(self, game: Dict, result: str):
        """Обновление профиля после игры
        
        Args:
            game: Данные игры
            result: Результат ('win', 'loss', 'draw')
        """
        self.games_played += 1
        self.last_game_at = datetime.now()
        
        # Обновление основной статистики
        if result == 'win':
            self.wins += 1
            self.win_streak += 1
            self.loss_streak = 0
            self.best_win_streak = max(self.best_win_streak, self.win_streak)
            self.last_win_at = datetime.now()
        elif result == 'loss':
            self.losses += 1
            self.loss_streak += 1
            self.win_streak = 0
        elif result == 'draw':
            self.draws += 1
            self.win_streak = 0
            self.loss_streak = 0
        
        # Статистика по цвету
        player_color = game.get('player_color', 'white')
        color_stats = self.white_stats if player_color == 'white' else self.black_stats
        color_stats['games'] += 1
        if result == 'win':
            color_stats['wins'] += 1
        elif result == 'loss':
            color_stats['losses'] += 1
        elif result == 'draw':
            color_stats['draws'] += 1
        
        # Статистика по режиму
        game_mode = game.get('game_mode', 'unknown')
        self.mode_stats[game_mode]['games'] += 1
        if result == 'win':
            self.mode_stats[game_mode]['wins'] += 1
        
        # Временная статистика
        if 'created_at' in game and 'ended_at' in game:
            game_duration = (game['ended_at'] - game['created_at']).total_seconds()
            self.total_time_played += game_duration
            self.shortest_game = min(self.shortest_game, game_duration)
            self.longest_game = max(self.longest_game, game_duration)
            self.average_game_time = self.total_time_played / self.games_played
        
        # Статистика ходов
        move_count = len(game.get('move_history', []))
        self.total_moves += move_count
        self.average_moves_per_game = self.total_moves / self.games_played
        
        # Дебютная статистика
        opening_info = opening_book.identify_opening(game.get('move_history', []))
        opening_name = opening_info.get('name', 'Unknown')
        self.opening_stats[opening_name]['games'] += 1
        if result == 'win':
            self.opening_stats[opening_name]['wins'] += 1
        elif result == 'loss':
            self.opening_stats[opening_name]['losses'] += 1
        elif result == 'draw':
            self.opening_stats[opening_name]['draws'] += 1
        
        # Обновление любимого дебюта
        self._update_favorite_opening()
        
        # Проверка достижений
        self._check_achievements()
    
    def _update_favorite_opening(self):
        """Обновление любимого дебюта"""
        if not self.opening_stats:
            return
        
        most_played = max(self.opening_stats.items(), key=lambda x: x[1]['games'])
        self.favorite_opening = {
            'name': most_played[0],
            'games': most_played[1]['games'],
            'win_rate': (most_played[1]['wins'] / most_played[1]['games'] * 100) if most_played[1]['games'] > 0 else 0
        }
    
    def _check_achievements(self):
        """Проверка и добавление достижений"""
        achievements_to_add = []
        
        # Достижения по количеству игр
        if self.games_played == 1:
            achievements_to_add.append({'name': 'First Game', 'description': 'Played your first game'})
        elif self.games_played == 10:
            achievements_to_add.append({'name': 'Beginner', 'description': 'Played 10 games'})
        elif self.games_played == 50:
            achievements_to_add.append({'name': 'Experienced', 'description': 'Played 50 games'})
        elif self.games_played == 100:
            achievements_to_add.append({'name': 'Veteran', 'description': 'Played 100 games'})
        
        # Достижения по победам
        if self.wins == 1:
            achievements_to_add.append({'name': 'First Victory', 'description': 'Won your first game'})
        elif self.wins == 10:
            achievements_to_add.append({'name': 'Winner', 'description': 'Won 10 games'})
        elif self.wins == 50:
            achievements_to_add.append({'name': 'Champion', 'description': 'Won 50 games'})
        
        # Достижения по сериям
        if self.win_streak == 3 and 'Triple Win' not in [a['name'] for a in self.achievements]:
            achievements_to_add.append({'name': 'Triple Win', 'description': 'Won 3 games in a row'})
        elif self.win_streak == 5 and 'Unstoppable' not in [a['name'] for a in self.achievements]:
            achievements_to_add.append({'name': 'Unstoppable', 'description': 'Won 5 games in a row'})
        elif self.win_streak == 10 and 'Legendary' not in [a['name'] for a in self.achievements]:
            achievements_to_add.append({'name': 'Legendary', 'description': 'Won 10 games in a row'})
        
        # Добавление новых достижений
        for achievement in achievements_to_add:
            if achievement not in self.achievements:
                achievement['earned_at'] = datetime.now().isoformat()
                self.achievements.append(achievement)
    
    def get_stats_summary(self) -> Dict:
        """Получение краткой статистики"""
        win_rate = (self.wins / self.games_played * 100) if self.games_played > 0 else 0
        
        return {
            'player_name': self.player_name,
            'games_played': self.games_played,
            'wins': self.wins,
            'losses': self.losses,
            'draws': self.draws,
            'win_rate': round(win_rate, 1),
            'current_streak': self.win_streak if self.win_streak > 0 else -self.loss_streak,
            'best_win_streak': self.best_win_streak,
            'total_time_played': round(self.total_time_played / 3600, 1),  # часы
            'average_game_time': round(self.average_game_time / 60, 1),  # минуты
            'average_moves': round(self.average_moves_per_game, 1),
            'favorite_opening': self.favorite_opening,
            'white_win_rate': round((self.white_stats['wins'] / self.white_stats['games'] * 100) if self.white_stats['games'] > 0 else 0, 1),
            'black_win_rate': round((self.black_stats['wins'] / self.black_stats['games'] * 100) if self.black_stats['games'] > 0 else 0, 1),
            'achievements_count': len(self.achievements),
            'last_game_at': self.last_game_at.isoformat() if self.last_game_at else None
        }
    
    def get_detailed_stats(self) -> Dict:
        """Получение детальной статистики"""
        summary = self.get_stats_summary()
        
        # Добавляем детальную информацию
        summary['white_stats'] = self.white_stats
        summary['black_stats'] = self.black_stats
        summary['mode_stats'] = dict(self.mode_stats)
        summary['opening_stats'] = self._get_top_openings(5)
        summary['achievements'] = self.achievements
        summary['created_at'] = self.created_at.isoformat()
        
        return summary
    
    def _get_top_openings(self, limit: int = 5) -> List[Dict]:
        """Получение топ дебютов"""
        top_openings = []
        for opening, stats in sorted(self.opening_stats.items(), key=lambda x: x[1]['games'], reverse=True)[:limit]:
            win_rate = (stats['wins'] / stats['games'] * 100) if stats['games'] > 0 else 0
            top_openings.append({
                'opening': opening,
                'games': stats['games'],
                'wins': stats['wins'],
                'losses': stats['losses'],
                'draws': stats['draws'],
                'win_rate': round(win_rate, 1)
            })
        return top_openings

class ProfileManager:
    """Менеджер профилей игроков"""
    def __init__(self):
        self.profiles: Dict[str, PlayerProfile] = {}
    
    def get_or_create_profile(self, player_name: str) -> PlayerProfile:
        """Получение или создание профиля"""
        if player_name not in self.profiles:
            self.profiles[player_name] = PlayerProfile(player_name)
        return self.profiles[player_name]
    
    def update_profile_from_game(self, player_name: str, game: Dict, result: str):
        """Обновление профиля после игры"""
        profile = self.get_or_create_profile(player_name)
        profile.update_from_game(game, result)
    
    def get_leaderboard(self, sort_by: str = 'win_rate', limit: int = 10) -> List[Dict]:
        """Таблица лидеров"""
        leaderboard = []
        for profile in self.profiles.values():
            if profile.games_played >= 5:  # Минимум 5 игр для лидерборда
                stats = profile.get_stats_summary()
                leaderboard.append(stats)
        
        # Сортировка
        if sort_by == 'win_rate':
            leaderboard.sort(key=lambda x: x['win_rate'], reverse=True)
        elif sort_by == 'wins':
            leaderboard.sort(key=lambda x: x['wins'], reverse=True)
        elif sort_by == 'games':
            leaderboard.sort(key=lambda x: x['games_played'], reverse=True)
        
        return leaderboard[:limit]

profile_manager = ProfileManager()

# Pydantic модели
class MoveRequest(BaseModel):
    game_id: str = Field(..., description="ID игры")
    from_pos: Tuple[int, int] = Field(..., description="Начальная позиция (row, col)")
    to_pos: Tuple[int, int] = Field(..., description="Конечная позиция (row, col)")
    player_color: bool = Field(..., description="Цвет игрока (True=белые, False=черные)")
    
    @field_validator('from_pos', 'to_pos')
    @classmethod
    def validate_position(cls, v):
        """Валидация позиции на доске"""
        if not (0 <= v[0] < 8 and 0 <= v[1] < 8):
            raise ValueError('Position must be between 0 and 7')
        return v

class GameRequest(BaseModel):
    player_name: str = Field(default="Anonymous", max_length=50, description="Имя игрока")
    game_mode: str = Field(default="ai", pattern="^(ai|human)$", description="Режим игры")
    player_color: bool = Field(default=True, description="Цвет игрока")
    time_control: int = Field(default=0, ge=0, le=60, description="Контроль времени в минутах (0=без ограничения)")
    
    @field_validator('player_name')
    @classmethod
    def validate_player_name(cls, v):
        """Валидация имени игрока"""
        if not v or v.strip() == "":
            return "Anonymous"
        return v.strip()

class GameResponse(BaseModel):
    game_id: str
    board_state: List[List[str]]
    current_turn: bool
    game_status: str
    move_history: List[Dict]
    player_name: str
    game_mode: str
    time_control: Optional[int] = 0
    white_time: Optional[float] = 0
    black_time: Optional[float] = 0

# HTML шаблоны
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Отображение главной страницы шахматного приложения"""
    try:
        with open("web/fastapi_index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Chess Web UI not found</h1><p>Please ensure web/fastapi_index.html exists.</p>"

@app.post("/api/new-game")
async def create_new_game(request: GameRequest):
    """Создание новой шахматной игры"""
    try:
        game_id = game_manager.create_game(
            request.player_name, 
            request.game_mode,
            request.time_control
        )
        game = game_manager.get_game(game_id)
        
        return GameResponse(
            game_id=game_id,
            board_state=game['engine'].board_state,
            current_turn=game['engine'].current_turn,
            game_status=game['game_status'],
            move_history=game['move_history'],
            player_name=request.player_name,
            game_mode=request.game_mode,
            time_control=game['time_control'],
            white_time=game['white_time'],
            black_time=game['black_time']
        )
    except Exception as e:
        logger.error(f"Error creating game: {e}")
        raise HTTPException(status_code=500, detail="Failed to create game")

@app.post("/api/make-move")
async def make_move(request: MoveRequest):
    """Выполнение хода в шахматной игре"""
    try:
        game = game_manager.get_game(request.game_id)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        
        # Обновление времени
        if game['time_control'] > 0 and game['move_start_time']:
            elapsed = time.time() - game['move_start_time']
            if game['engine'].current_turn:  # Белые
                game['white_time'] = max(0, game['white_time'] - elapsed)
                if game['white_time'] <= 0:
                    game['game_status'] = 'time_out'
                    game['winner'] = 'black'
                    return {
                        'success': False,
                        'message': 'White time out',
                        'game_status': 'time_out',
                        'winner': 'black'
                    }
            else:  # Черные
                game['black_time'] = max(0, game['black_time'] - elapsed)
                if game['black_time'] <= 0:
                    game['game_status'] = 'time_out'
                    game['winner'] = 'white'
                    return {
                        'success': False,
                        'message': 'Black time out',
                        'game_status': 'time_out',
                        'winner': 'white'
                    }
        
        engine = game['engine']
        from_pos = tuple(request.from_pos)
        to_pos = tuple(request.to_pos)
        
        # Выполнение хода через движок
        success = engine.make_move(from_pos, to_pos)
        
        if success:
            # Запись хода для веб UI
            move_record = {
                'from': from_pos,
                'to': to_pos,
                'piece': engine.board_state[to_pos[0]][to_pos[1]],
                'notation': engine.move_history[-1] if engine.move_history else "",
                'timestamp': datetime.now().isoformat()
            }
            game['move_history'].append(move_record)
            
            # Запись в PGN рекордер с SAN нотацией
            if request.game_id in game_manager.game_recorders:
                recorder = game_manager.game_recorders[request.game_id]
                is_capture = engine.board_state[to_pos[0]][to_pos[1]] != '.'
                san_notation = san_parser.move_to_san(
                    from_pos, to_pos, move_record['piece'], 
                    engine.board_state, is_capture
                )
                recorder.add_move(san_notation)
            
            # Определение статуса игры (мат, пат, ничья)
            if engine.is_checkmate():
                game['game_status'] = 'checkmate'
                game['winner'] = 'black' if engine.current_turn else 'white'
                # Запись результата в PGN
                if request.game_id in game_manager.game_recorders:
                    result = "0-1" if engine.current_turn else "1-0"
                    game_manager.game_recorders[request.game_id].set_result(result)
            elif engine.is_stalemate():
                game['game_status'] = 'stalemate'
                game['winner'] = 'draw'
                # Запись результата в PGN
                if request.game_id in game_manager.game_recorders:
                    game_manager.game_recorders[request.game_id].set_result("1/2-1/2")
            else:
                game['game_status'] = 'active'
            
            # Сброс таймера для следующего хода
            if game['time_control'] > 0:
                game['move_start_time'] = time.time()
            
            return {
                'success': True,
                'game_state': GameResponse(
                    game_id=request.game_id,
                    board_state=engine.board_state,
                    current_turn=engine.current_turn,
                    game_status="active",
                    move_history=game['move_history'],
                    player_name=game['player_name'],
                    game_mode=game['game_mode'],
                    time_control=game['time_control'],
                    white_time=game['white_time'],
                    black_time=game['black_time']
                )
            }
        else:
            return {
                'success': False,
                'message': 'Invalid move'
            }
            
    except Exception as e:
        logger.error(f"Error making move: {e}")
        return {'success': False, 'message': str(e)}

@app.get("/api/valid-moves/{game_id}")
async def get_valid_moves(game_id: str, r: int, c: int):
    """Получение допустимых ходов для фигуры на (r, c)"""
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
    """Получение оценки позиции"""
    game = game_manager.get_game(game_id)
    if not game:
        return {"evaluation": 0}
    
    return {"evaluation": game['engine'].get_evaluation()}

@app.get("/api/time/{game_id}")
async def get_time(game_id: str):
    """Получение текущего времени игроков"""
    game = game_manager.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    # Обновление времени текущего игрока
    if game['time_control'] > 0 and game['move_start_time']:
        elapsed = time.time() - game['move_start_time']
        if game['engine'].current_turn:
            current_time = max(0, game['white_time'] - elapsed)
        else:
            current_time = max(0, game['black_time'] - elapsed)
    else:
        current_time = 0
    
    return {
        "time_control": game['time_control'],
        "white_time": game['white_time'],
        "black_time": game['black_time'],
        "current_turn": game['engine'].current_turn,
        "elapsed": elapsed if game['time_control'] > 0 and game['move_start_time'] else 0
    }

@app.get("/api/ai-move/{game_id}")
async def get_ai_move(game_id: str, depth: int = 4):
    """Получение хода AI для текущей позиции"""
    try:
        game = game_manager.get_game(game_id)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        
        engine = game['engine']
        
        # Генерация ключа кэша на основе состояния доски
        board_hash = hash(str(engine.board_state) + str(engine.current_turn) + str(depth))
        cache_key = f"{game_id}_{board_hash}"
        
        # Проверка кэша
        cached_result = move_cache.get(cache_key)
        if cached_result:
            logger.info(f"Cache hit for game {game_id}")
            return cached_result
        
        # Вычисление нового хода
        start_time = time.time()
        best_move = engine.get_best_move(depth=depth)
        calculation_time = time.time() - start_time
        
        if best_move:
            from_pos, to_pos = best_move
            engine.make_move(from_pos, to_pos)
            
            # Запись хода
            move_record = {
                'from': from_pos,
                'to': to_pos,
                'piece': engine.board_state[to_pos[0]][to_pos[1]],
                'notation': engine.move_history[-1] if engine.move_history else "",
                'timestamp': datetime.now().isoformat()
            }
            game['move_history'].append(move_record)
            
            result = {
                'success': True,
                'move_notation': move_record['notation'],
                'calculation_time': round(calculation_time, 3),
                'ai_stats': engine.get_game_statistics(),
                'game_state': GameResponse(
                    game_id=game_id,
                    board_state=engine.board_state,
                    current_turn=engine.current_turn,
                    game_status="active",
                    move_history=game['move_history'],
                    player_name=game['player_name'],
                    game_mode=game['game_mode'],
                    time_control=game['time_control'],
                    white_time=game['white_time'],
                    black_time=game['black_time']
                )
            }
            
            # Сброс таймера для следующего хода
            if game['time_control'] > 0:
                game['move_start_time'] = time.time()
            
            # Сохранение в кэш
            move_cache.set(cache_key, result)
            logger.info(f"AI move calculated in {calculation_time:.3f}s for game {game_id}")
            
            return result
        return {"success": False, "message": "No moves available"}
    except Exception as e:
        logger.error(f"AI Move Error: {e}")
        return {"success": False, "message": str(e)}

@app.post("/api/save-game/{game_id}")
async def save_game(game_id: str):
    """Сохранение текущего состояния игры в файл"""
    game = game_manager.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    success = game['engine'].save_game("web_chess_save.json")
    return {"success": success}

@app.post("/api/load-game")
async def load_game():
    """Загрузка состояния игры из файла"""
    # На данный момент загружаем в новую сессию игры
    game_id = game_manager.create_game("Loaded Player", "ai")
    game = game_manager.get_game(game_id)
    
    success = game['engine'].load_game("web_chess_save.json")
    if success:
        # Обновление истории ходов из движка при необходимости
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
    """Отмена последнего хода"""
    try:
        game = game_manager.get_game(game_id)
        if not game:
            return {'success': False, 'message': 'Game not found'}
        
        if not game['move_history']:
            return {'success': False, 'message': 'No moves to undo'}
        
        # Используем функционал отмены движка, если доступен
        engine = game['engine']
        if hasattr(engine, 'undo_last_move') and callable(engine.undo_last_move):
            success = engine.undo_last_move()
            if success:
                game['move_history'].pop()
        else:
            # Fallback: ручная отмена
            last_move = game['move_history'].pop()
            engine.board_state[last_move['from'][0]][last_move['from'][1]] = last_move['piece']
            engine.board_state[last_move['to'][0]][last_move['to'][1]] = last_move.get('captured', '.')
            engine.current_turn = not engine.current_turn
        
        return {
            'success': True,
            'game_state': GameResponse(
                game_id=game_id,
                board_state=engine.board_state,
                current_turn=engine.current_turn,
                game_status='active',
                move_history=game['move_history'],
                player_name=game['player_name'],
                game_mode=game['game_mode']
            )
        }
        
    except Exception as e:
        logger.error(f"Error undoing move: {e}")
        return {'success': False, 'message': str(e)}

def check_game_status(board: List[List[str]], current_turn: bool) -> str:
    """Проверка текущего статуса игры"""
    # Это упрощенная реализация
    # В полной реализации нужно проверять шах, мат, пат
    return "active"

def convert_to_algebraic(from_pos: Tuple[int, int], to_pos: Tuple[int, int], piece: str) -> str:
    """Преобразование координат хода в алгебраическую нотацию"""
    files = 'abcdefgh'
    ranks = '87654321'
    
    from_square = files[from_pos[1]] + ranks[from_pos[0]]
    to_square = files[to_pos[1]] + ranks[to_pos[0]]
    
    piece_symbol = piece.upper() if piece.isupper() else piece.lower()
    return f"{piece_symbol}{from_square}-{to_square}"

def calculate_material_balance(board_state: List[List[str]]) -> Dict:
    """Расчет материального баланса"""
    piece_values = {
        'p': 1, 'P': 1,
        'n': 3, 'N': 3,
        'b': 3, 'B': 3,
        'r': 5, 'R': 5,
        'q': 9, 'Q': 9
    }
    
    white_material = 0
    black_material = 0
    white_pieces = {'pawns': 0, 'knights': 0, 'bishops': 0, 'rooks': 0, 'queens': 0}
    black_pieces = {'pawns': 0, 'knights': 0, 'bishops': 0, 'rooks': 0, 'queens': 0}
    
    for row in board_state:
        for piece in row:
            if piece in piece_values:
                if piece.isupper():
                    white_material += piece_values[piece]
                    if piece == 'P': white_pieces['pawns'] += 1
                    elif piece == 'N': white_pieces['knights'] += 1
                    elif piece == 'B': white_pieces['bishops'] += 1
                    elif piece == 'R': white_pieces['rooks'] += 1
                    elif piece == 'Q': white_pieces['queens'] += 1
                else:
                    black_material += piece_values[piece]
                    if piece == 'p': black_pieces['pawns'] += 1
                    elif piece == 'n': black_pieces['knights'] += 1
                    elif piece == 'b': black_pieces['bishops'] += 1
                    elif piece == 'r': black_pieces['rooks'] += 1
                    elif piece == 'q': black_pieces['queens'] += 1
    
    return {
        'white': white_material,
        'black': black_material,
        'balance': white_material - black_material,
        'white_pieces': white_pieces,
        'black_pieces': black_pieces
    }

def determine_game_phase(board_state: List[List[str]], move_count: int) -> str:
    """Определение фазы игры"""
    material = calculate_material_balance(board_state)
    total_material = material['white'] + material['black']
    
    if move_count < 10:
        return 'opening'
    elif total_material > 40:
        return 'middlegame'
    elif total_material > 20:
        return 'late_middlegame'
    else:
        return 'endgame'

def analyze_threats(board_state: List[List[str]], current_turn: bool) -> List[str]:
    """Анализ тактических угроз"""
    threats = []
    
    # Упрощенный анализ - можно расширить
    # Проверка на открытые линии атаки
    
    return threats

def analyze_center_control(board_state: List[List[str]]) -> Dict:
    """Анализ контроля центра"""
    # Центральные клетки (d4, d5, e4, e5)
    center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
    extended_center = [(2, 2), (2, 3), (2, 4), (2, 5), 
                       (3, 2), (3, 5), (4, 2), (4, 5),
                       (5, 2), (5, 3), (5, 4), (5, 5)]
    
    white_center = 0
    black_center = 0
    
    for r, c in center_squares:
        piece = board_state[r][c]
        if piece != '.':
            if piece.isupper():
                white_center += 2
            else:
                black_center += 2
    
    for r, c in extended_center:
        piece = board_state[r][c]
        if piece != '.':
            if piece.isupper():
                white_center += 1
            else:
                black_center += 1
    
    return {
        'white': white_center,
        'black': black_center,
        'advantage': 'white' if white_center > black_center else 'black' if black_center > white_center else 'equal'
    }

def analyze_king_safety(board_state: List[List[str]]) -> Dict:
    """Анализ безопасности короля"""
    # Поиск королей
    white_king_pos = None
    black_king_pos = None
    
    for r in range(8):
        for c in range(8):
            if board_state[r][c] == 'K':
                white_king_pos = (r, c)
            elif board_state[r][c] == 'k':
                black_king_pos = (r, c)
    
    def king_safety_score(king_pos, is_white):
        if not king_pos:
            return 0
        
        r, c = king_pos
        safety = 5  # Базовая безопасность
        
        # Проверка пешечной защиты
        pawn = 'P' if is_white else 'p'
        direction = -1 if is_white else 1
        
        for dc in [-1, 0, 1]:
            nr, nc = r + direction, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                if board_state[nr][nc] == pawn:
                    safety += 1
        
        # Пенальти за центральное положение в миттельшпиле
        if 2 <= r <= 5 and 2 <= c <= 5:
            safety -= 2
        
        # Бонус за рокировку (король в углу)
        if (c <= 2 or c >= 5) and ((is_white and r == 7) or (not is_white and r == 0)):
            safety += 2
        
        return max(0, min(10, safety))  # Ограничение 0-10
    
    return {
        'white': king_safety_score(white_king_pos, True),
        'black': king_safety_score(black_king_pos, False),
        'white_king_position': white_king_pos,
        'black_king_position': black_king_pos
    }

def get_evaluation_text(evaluation: float) -> str:
    """Преобразование числовой оценки в текст"""
    if evaluation > 300:
        return "White is winning"
    elif evaluation > 100:
        return "White has a significant advantage"
    elif evaluation > 50:
        return "White has a slight advantage"
    elif evaluation > -50:
        return "Equal position"
    elif evaluation > -100:
        return "Black has a slight advantage"
    elif evaluation > -300:
        return "Black has a significant advantage"
    else:
        return "Black is winning"

# WebSocket endpoint для real-time обновлений
@app.websocket("/ws/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str):
    """WebSocket endpoint для real-time обновлений игры с поддержкой переподключения"""
    await websocket.accept()
    connection_id = str(uuid.uuid4())
    logger.info(f"WebSocket connected: {connection_id} for game {game_id}")
    
    try:
        # Добавление подключения к игре
        if game_id in game_manager.connections:
            game_manager.connections[game_id].append(websocket)
        else:
            game_manager.connections[game_id] = [websocket]
        
        # Отправка начального состояния
        game = game_manager.get_game(game_id)
        if game:
            await websocket.send_json({
                'type': 'connected',
                'connection_id': connection_id,
                'game_state': {
                    'board': game['engine'].board_state,
                    'turn': game['engine'].current_turn,
                    'status': game['game_status']
                }
            })
        
        # Обработка входящих сообщений
        while True:
            try:
                data = await asyncio.wait_for(websocket.receive_json(), timeout=30.0)
                
                # Обработка ping для keep-alive
                if data.get('type') == 'ping':
                    await websocket.send_json({'type': 'pong', 'timestamp': time.time()})
                    
                # Обработка запроса на синхронизацию
                elif data.get('type') == 'sync':
                    game = game_manager.get_game(game_id)
                    if game:
                        await websocket.send_json({
                            'type': 'sync_response',
                            'game_state': {
                                'board': game['engine'].board_state,
                                'turn': game['engine'].current_turn,
                                'status': game['game_status'],
                                'move_history': game['move_history']
                            }
                        })
                        
            except asyncio.TimeoutError:
                # Проверка соединения через ping
                try:
                    await websocket.send_json({'type': 'ping'})
                except:
                    break
            except Exception as e:
                logger.error(f"WebSocket error in message loop: {e}")
                break
                    
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected: {connection_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        # Удаление подключения
        if game_id in game_manager.connections:
            if websocket in game_manager.connections[game_id]:
                game_manager.connections[game_id].remove(websocket)
                logger.info(f"WebSocket connection removed: {connection_id}")

@app.post("/api/save-game/{game_id}")
async def save_game_endpoint(game_id: str):
    """Сохранение текущей игры"""
    try:
        game = game_manager.get_game(game_id)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        
        # Создание директории для сохраненных игр
        saves_dir = os.path.join(os.path.dirname(__file__), '..', 'saved_games')
        os.makedirs(saves_dir, exist_ok=True)
        
        # Сохранение данных игры
        save_data = {
            'game_id': game_id,
            'player_name': game['player_name'],
            'game_mode': game['game_mode'],
            'board_state': game['engine'].board_state,
            'current_turn': game['engine'].current_turn,
            'move_history': game['move_history'],
            'captured_pieces': game['engine'].captured_pieces if hasattr(game['engine'], 'captured_pieces') else {'white': [], 'black': []},
            'game_status': game['game_status'],
            'time_control': game['time_control'],
            'white_time': game['white_time'],
            'black_time': game['black_time'],
            'created_at': game['created_at'].isoformat(),
            'saved_at': datetime.now().isoformat()
        }
        
        filename = os.path.join(saves_dir, f"{game_id}.json")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Game {game_id} saved to {filename}")
        return {
            'success': True,
            'message': 'Game saved successfully',
            'filename': f"{game_id}.json"
        }
        
    except Exception as e:
        logger.error(f"Error saving game: {e}")
        raise HTTPException(status_code=500, detail="Failed to save game")

@app.post("/api/load-game/{save_id}")
async def load_game_endpoint(save_id: str):
    """Загрузка сохраненной игры"""
    try:
        saves_dir = os.path.join(os.path.dirname(__file__), '..', 'saved_games')
        filename = os.path.join(saves_dir, f"{save_id}.json")
        
        if not os.path.exists(filename):
            raise HTTPException(status_code=404, detail="Save file not found")
        
        with open(filename, 'r', encoding='utf-8') as f:
            save_data = json.load(f)
        
        # Создание новой игры на основе сохраненных данных
        new_game_id = str(uuid.uuid4())
        engine = ChessEngineWrapper()
        engine.board_state = save_data['board_state']
        engine.current_turn = save_data['current_turn']
        engine.move_history = save_data.get('move_history', [])
        if hasattr(engine, 'captured_pieces'):
            engine.captured_pieces = save_data.get('captured_pieces', {'white': [], 'black': []})
        
        game_manager.games[new_game_id] = {
            'id': new_game_id,
            'player_name': save_data.get('player_name', 'Anonymous'),
            'game_mode': save_data.get('game_mode', 'ai'),
            'engine': engine,
            'ai': EnhancedChessAI(search_depth=4) if save_data.get('game_mode') == 'ai' else None,
            'move_generator': BitboardMoveGenerator(),
            'created_at': datetime.fromisoformat(save_data['created_at']),
            'last_move_time': datetime.now(),
            'move_history': save_data.get('move_history', []),
            'current_player': save_data['current_turn'],
            'game_status': save_data.get('game_status', 'active'),
            'winner': None,
            'time_control': save_data.get('time_control', 0),
            'white_time': save_data.get('white_time', 0),
            'black_time': save_data.get('black_time', 0),
            'move_start_time': time.time() if save_data.get('time_control', 0) > 0 else None
        }
        game_manager.connections[new_game_id] = []
        
        logger.info(f"Game loaded from {filename} as new game {new_game_id}")
        return {
            'success': True,
            'game_id': new_game_id,
            'game_state': GameResponse(
                game_id=new_game_id,
                board_state=engine.board_state,
                current_turn=engine.current_turn,
                game_status=save_data.get('game_status', 'active'),
                move_history=save_data.get('move_history', []),
                player_name=save_data.get('player_name', 'Anonymous'),
                game_mode=save_data.get('game_mode', 'ai'),
                time_control=save_data.get('time_control', 0),
                white_time=save_data.get('white_time', 0),
                black_time=save_data.get('black_time', 0)
            )
        }
        
    except Exception as e:
        logger.error(f"Error loading game: {e}")
        raise HTTPException(status_code=500, detail="Failed to load game")

@app.get("/api/saved-games")
async def list_saved_games():
    """Получение списка сохраненных игр"""
    try:
        saves_dir = os.path.join(os.path.dirname(__file__), '..', 'saved_games')
        if not os.path.exists(saves_dir):
            return {'saved_games': [], 'total': 0}
        
        saved_games = []
        for filename in os.listdir(saves_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(saves_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    saved_games.append({
                        'save_id': filename.replace('.json', ''),
                        'player_name': data.get('player_name', 'Unknown'),
                        'game_mode': data.get('game_mode', 'unknown'),
                        'moves_count': len(data.get('move_history', [])),
                        'saved_at': data.get('saved_at', ''),
                        'game_status': data.get('game_status', 'unknown')
                    })
                except:
                    continue
        
        # Сортировка по дате сохранения
        saved_games.sort(key=lambda x: x.get('saved_at', ''), reverse=True)
        
        return {'saved_games': saved_games, 'total': len(saved_games)}
        
    except Exception as e:
        logger.error(f"Error listing saved games: {e}")
        return {'saved_games': [], 'total': 0}

@app.get("/health")
async def health_check():
    """Проверка здоровья системы"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_games": len(game_manager.games),
        "cache_size": len(move_cache.cache),
        "version": "2.0.0"
    }

@app.get("/api/games")
async def list_active_games():
    """Получение списка активных игр"""
    games_list = []
    for game_id, game_data in game_manager.games.items():
        games_list.append({
            'game_id': game_id,
            'player_name': game_data['player_name'],
            'game_mode': game_data['game_mode'],
            'created_at': game_data['created_at'].isoformat(),
            'moves_count': len(game_data['move_history']),
            'status': game_data['game_status']
        })
    return {"games": games_list, "total": len(games_list)}

@app.delete("/api/game/{game_id}")
async def delete_game_endpoint(game_id: str):
    """Удаление игры"""
    if game_id not in game_manager.games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game_manager.delete_game(game_id)
    return {"success": True, "message": f"Game {game_id} deleted"}

@app.post("/api/clear-cache")
async def clear_cache():
    """Очистка кэша AI ходов"""
    move_cache.clear()
    return {"success": True, "message": "Cache cleared"}

@app.get("/api/stats/{game_id}")
async def get_stats(game_id: str):
    """Получение статистики игры"""
    try:
        game = game_manager.get_game(game_id)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        
        engine = game['engine']
        stats = {
            'total_moves': len(game['move_history']),
            'captures': sum(1 for m in game['move_history'] if m.get('captured')),
            'game_duration': (datetime.now() - game['created_at']).total_seconds(),
            'current_evaluation': engine.get_evaluation() if hasattr(engine, 'get_evaluation') else 0
        }
        
        # Добавление статистики движка, если доступно
        if hasattr(engine, 'get_game_statistics'):
            engine_stats = engine.get_game_statistics()
            stats.update(engine_stats)
        
        return stats
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get stats")

@app.get("/api/game/{game_id}/export_pgn")
async def export_pgn(game_id: str):
    """Экспорт игры в формат PGN"""
    try:
        game = game_manager.get_game(game_id)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        
        # Получение PGN из рекордера
        if game_id not in game_manager.game_recorders:
            raise HTTPException(status_code=404, detail="PGN recorder not found for this game")
        
        recorder = game_manager.game_recorders[game_id]
        pgn_content = recorder.get_pgn()
        
        # Возврат PGN как текстового файла
        return PlainTextResponse(
            content=pgn_content,
            headers={
                'Content-Disposition': f'attachment; filename="game_{game_id[:8]}.pgn"',
                'Content-Type': 'application/x-chess-pgn'
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error exporting PGN: {e}")
        raise HTTPException(status_code=500, detail="Failed to export PGN")

@app.get("/api/game/{game_id}/analyze")
async def analyze_position(game_id: str, depth: int = 3):
    """Анализ текущей позиции с подробной информацией"""
    try:
        game = game_manager.get_game(game_id)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        
        engine = game['engine']
        
        # Получение базовой оценки
        evaluation = engine.get_evaluation() if hasattr(engine, 'get_evaluation') else 0
        
        # Получение лучших ходов
        best_moves = []
        if hasattr(engine, 'get_best_move'):
            best_move = engine.get_best_move(depth=depth)
            if best_move:
                best_moves.append({
                    'from': best_move[0],
                    'to': best_move[1],
                    'notation': f"{best_move[0]}-{best_move[1]}"
                })
        
        # Анализ материала
        material_balance = calculate_material_balance(engine.board_state)
        
        # Определение фазы игры
        game_phase = determine_game_phase(engine.board_state, len(game['move_history']))
        
        # Определение дебюта
        opening_info = opening_book.identify_opening(game['move_history'])
        
        # Тактические угрозы
        threats = analyze_threats(engine.board_state, engine.current_turn)
        
        # Контроль центра
        center_control = analyze_center_control(engine.board_state)
        
        # Безопасность короля
        king_safety = analyze_king_safety(engine.board_state)
        
        # Проверка эндшпиля
        endgame_result = None
        if material_balance['white'] + material_balance['black'] <= 10:
            # Преобразуем в формат tablebase
            pieces = {}
            for r in range(8):
                for c in range(8):
                    piece = engine.board_state[r][c]
                    if piece != '.':
                        file = 'abcdefgh'[c]
                        rank = str(r + 1)
                        pieces[file + rank] = piece
            
            board_for_tb = {
                'pieces': pieces,
                'turn': 'white' if engine.current_turn else 'black'
            }
            
            if endgame_tablebase.is_applicable(board_for_tb):
                endgame_result = endgame_tablebase.get_result(board_for_tb)
        
        # Проверка мата и пата
        is_mate = engine.is_checkmate(engine.current_turn)
        is_stalemate = engine.is_stalemate(engine.current_turn)
        is_check = engine.is_king_in_check(engine.current_turn)
        
        return {
            'game_id': game_id,
            'evaluation': evaluation,
            'evaluation_text': get_evaluation_text(evaluation),
            'best_moves': best_moves,
            'material_balance': material_balance,
            'game_phase': game_phase,
            'opening': opening_info,
            'threats': threats,
            'center_control': center_control,
            'king_safety': king_safety,
            'endgame_result': endgame_result,
            'is_checkmate': is_mate,
            'is_stalemate': is_stalemate,
            'is_check': is_check,
            'move_count': len(game['move_history']),
            'current_turn': 'white' if engine.current_turn else 'black'
        }
        
    except Exception as e:
        logger.error(f"Error analyzing position: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze position")

@app.post("/api/game/import_pgn")
async def import_pgn(request: Request):
    """Импорт игры из формата PGN"""
    try:
        # Получение содержимого PGN из тела запроса
        body = await request.body()
        pgn_content = body.decode('utf-8')
        
        if not pgn_content:
            raise HTTPException(status_code=400, detail="Empty PGN content")
        
        # Парсинг PGN с помощью PGNSaver
        parsed_game = game_manager.pgn_saver.parse_pgn(pgn_content)
        
        if not parsed_game:
            raise HTTPException(status_code=400, detail="Failed to parse PGN")
        
        # Создание новой игры
        new_game_id = str(uuid.uuid4())
        white_player = parsed_game.get('white', 'Player1')
        black_player = parsed_game.get('black', 'Player2')
        
        # Инициализация движка
        engine = ChessEngineWrapper()
        
        # Создание игры
        game_manager.games[new_game_id] = {
            'id': new_game_id,
            'player_name': white_player,
            'game_mode': 'replay',
            'engine': engine,
            'ai': None,
            'move_generator': BitboardMoveGenerator(),
            'created_at': datetime.now(),
            'last_move_time': datetime.now(),
            'move_history': [],
            'current_player': True,
            'game_status': parsed_game.get('result', 'active'),
            'winner': None,
            'time_control': 0,
            'white_time': 0,
            'black_time': 0,
            'move_start_time': None
        }
        game_manager.connections[new_game_id] = []
        
        # Инициализация PGN рекордера
        recorder = GameRecorder()
        recorder.start_recording(white_player=white_player, black_player=black_player)
        game_manager.game_recorders[new_game_id] = recorder
        
        # Применение ходов из PGN
        moves = parsed_game.get('moves', [])
        game = game_manager.games[new_game_id]
        
        for move_notation in moves:
            # Попытка применить ход (это упрощенная версия, может потребоваться доработка)
            # В реальности нужен парсер алгебраической нотации
            try:
                # Добавляем ход в историю
                move_record = {
                    'notation': move_notation,
                    'timestamp': datetime.now().isoformat()
                }
                game['move_history'].append(move_record)
                recorder.add_move(move_notation)
            except Exception as e:
                logger.warning(f"Failed to apply move {move_notation}: {e}")
                continue
        
        # Установка результата
        result = parsed_game.get('result', '*')
        if result != '*':
            recorder.set_result(result)
            if result == '1-0':
                game['game_status'] = 'checkmate'
                game['winner'] = 'white'
            elif result == '0-1':
                game['game_status'] = 'checkmate'
                game['winner'] = 'black'
            elif result == '1/2-1/2':
                game['game_status'] = 'draw'
                game['winner'] = 'draw'
        
        logger.info(f"PGN imported as game {new_game_id}")
        return {
            'success': True,
            'game_id': new_game_id,
            'message': f'Successfully imported PGN with {len(moves)} moves',
            'white_player': white_player,
            'black_player': black_player,
            'result': result,
            'moves_count': len(moves)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error importing PGN: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to import PGN: {str(e)}")

@app.get("/api/player-stats/{player_name}")
async def get_player_stats(player_name: str):
    """Получение статистики игрока"""
    stats = player_stats.get_stats(player_name)
    
    # Форматирование времени
    if stats['shortest_game'] == float('inf'):
        stats['shortest_game'] = 0
    
    return {
        'player': player_name,
        'games_played': stats['games_played'],
        'wins': stats['wins'],
        'losses': stats['losses'],
        'draws': stats['draws'],
        'win_rate': round(stats['win_rate'], 2),
        'total_moves': stats['total_moves'],
        'avg_game_time': round(stats['avg_game_time'], 1),
        'longest_game': round(stats['longest_game'], 1),
        'shortest_game': round(stats['shortest_game'], 1)
    }

@app.get("/api/leaderboard")
async def get_leaderboard(limit: int = 10):
    """Получение таблицы лидеров"""
    leaderboard = player_stats.get_leaderboard(limit)
    return {
        "leaderboard": leaderboard,
        "total_players": len(player_stats.stats)
    }

@app.post("/api/end-game/{game_id}")
async def end_game(game_id: str, winner: Optional[str] = None):
    """Завершение игры и обновление статистики"""
    game = game_manager.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game['ended_at'] = datetime.now()
    game['winner'] = winner
    game['game_status'] = 'finished'
    
    # Определение результата
    player_name = game['player_name']
    if winner == player_name:
        result = 'win'
    elif winner is None:
        result = 'draw'
    else:
        result = 'loss'
    
    # Обновление старой статистики
    player_stats.update_stats(player_name, game)
    
    # Обновление профиля игрока
    profile_manager.update_profile_from_game(player_name, game, result)
    
    # Добавление в историю
    game_history.add_game(game)
    
    # Обновление ELO рейтинга
    rating_update = None
    if game['game_mode'] == 'ai':
        ai_ratings = {2: 1000, 3: 1400, 4: 1600, 5: 1800}
        ai_depth = getattr(game.get('ai'), 'search_depth', 4) if game.get('ai') else 4
        opponent_rating = ai_ratings.get(ai_depth, 1600)
        
        actual_score = 1.0 if winner == game['player_name'] else (0.5 if winner is None else 0.0)
        
        rating_update = elo_system.update_ratings(
            player_name=game['player_name'],
            opponent_rating=opponent_rating,
            actual_score=actual_score,
            game_id=game_id
        )
        rating_update['rank'] = elo_system.get_rank_title(rating_update['new_rating'])
    
    return {
        "success": True,
        "winner": winner,
        "game_duration": (game['ended_at'] - game['created_at']).total_seconds(),
        "total_moves": len(game['move_history']),
        "rating_update": rating_update
    }

@app.get("/api/game-history")
async def get_game_history(limit: int = 10):
    """Получение истории игр"""
    recent_games = game_history.get_recent_games(limit)
    return {
        "games": recent_games,
        "total": len(game_history.games)
    }

@app.get("/api/player-history/{player_name}")
async def get_player_history(player_name: str, limit: int = 10):
    """Получение истории игр игрока"""
    player_games = game_history.get_player_games(player_name, limit)
    return {
        "player": player_name,
        "games": player_games,
        "total": len(player_games)
    }

@app.get("/api/export-pgn/{game_id}")
async def export_game_pgn(game_id: str):
    """Экспорт игры в формат PGN"""
    pgn = game_history.export_to_pgn(game_id)
    if not pgn:
        raise HTTPException(status_code=404, detail="Game not found in history")
    
    return PlainTextResponse(
        content=pgn,
        media_type="application/x-chess-pgn",
        headers={"Content-Disposition": f"attachment; filename=chess_game_{game_id[:8]}.pgn"}
    )

@app.post("/api/analyze-game/{game_id}")
async def analyze_game(game_id: str):
    """Анализ завершенной игры"""
    # Поиск в истории
    game_data = next((g for g in game_history.games if g['game_id'] == game_id), None)
    
    if not game_data:
        # Проверка активных игр
        game = game_manager.get_game(game_id)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        game_data = game
    
    try:
        analysis = game_analyzer.analyze_game(game_data)
        return {
            "success": True,
            "game_id": game_id,
            "analysis": analysis
        }
    except Exception as e:
        logger.error(f"Error analyzing game: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/api/position-insights/{game_id}")
async def get_position_insights(game_id: str):
    """Получение подсказок для текущей позиции"""
    game = game_manager.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    try:
        board_state = game['engine'].get_board()
        is_white = game['current_player']
        insights = game_analyzer.get_position_insights(board_state, is_white)
        
        return {
            "success": True,
            "insights": insights
        }
    except Exception as e:
        logger.error(f"Error getting position insights: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get insights: {str(e)}")

@app.post("/api/analyze-position/{game_id}")
async def analyze_position(game_id: str, depth: int = 3):
    """Глубокий анализ текущей позиции с тактическими инсайтами"""
    game = game_manager.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    try:
        engine = game['engine']
        board_state = engine.board_state
        current_turn = engine.current_turn
        
        # Анализ материала
        material_analysis = analyze_material(board_state)
        
        # Анализ контроля центра
        center_control = analyze_center_control(board_state)
        
        # Поиск тактических мотивов
        tactical_motifs = find_tactical_motifs(board_state, current_turn, engine)
        
        # Анализ безопасности королей
        king_safety = analyze_king_safety(board_state, current_turn, engine)
        
        # Анализ структуры пешек
        pawn_structure = analyze_pawn_structure(board_state)
        
        # Получение лучших ходов
        best_moves = get_top_moves(engine, board_state, current_turn, depth, top_n=3)
        
        # Общая оценка позиции
        position_eval = evaluate_position(board_state, current_turn)
        
        return {
            "success": True,
            "analysis": {
                "evaluation": position_eval,
                "material": material_analysis,
                "center_control": center_control,
                "tactical_motifs": tactical_motifs,
                "king_safety": king_safety,
                "pawn_structure": pawn_structure,
                "best_moves": best_moves
            }
        }
    except Exception as e:
        logger.error(f"Error analyzing position: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/api/elo-rating/{player_name}")
async def get_elo_rating(player_name: str):
    """Получение ELO рейтинга игрока"""
    rating = elo_system.get_rating(player_name)
    rank_title = elo_system.get_rank_title(rating)
    history = elo_system.get_rating_history(player_name, limit=10)
    
    return {
        "player": player_name,
        "rating": rating,
        "rank": rank_title,
        "games_played": len(history),
        "recent_history": history
    }

@app.get("/api/elo-leaderboard")
async def get_elo_leaderboard(limit: int = 10):
    """Получение таблицы лидеров по ELO"""
    leaderboard = elo_system.get_leaderboard(limit)
    
    # Добавление званий
    for entry in leaderboard:
        entry['rank'] = elo_system.get_rank_title(entry['rating'])
    
    return {
        "leaderboard": leaderboard,
        "total_players": len(elo_system.ratings)
    }

@app.post("/api/update-elo/{game_id}")
async def update_elo_rating(game_id: str, winner: Optional[str] = None):
    """Обновление ELO рейтинга после игры"""
    game = game_manager.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    player_name = game['player_name']
    
    # Рейтинг AI в зависимости от сложности
    ai_ratings = {
        2: 1000,  # Novice
        3: 1400,  # Casual
        4: 1600,  # Pro
        5: 1800   # Master
    }
    
    ai_depth = 4  # По умолчанию
    if game['ai']:
        ai_depth = getattr(game['ai'], 'search_depth', 4)
    
    opponent_rating = ai_ratings.get(ai_depth, 1600)
    
    # Определение результата
    if winner == player_name:
        actual_score = 1.0
    elif winner is None:
        actual_score = 0.5  # Ничья
    else:
        actual_score = 0.0
    
    # Обновление рейтинга
    rating_update = elo_system.update_ratings(
        player_name=player_name,
        opponent_rating=opponent_rating,
        actual_score=actual_score,
        game_id=game_id
    )
    
    rating_update['rank'] = elo_system.get_rank_title(rating_update['new_rating'])
    
    return {
        "success": True,
        "rating_update": rating_update
    }

@app.get("/api/opening/{game_id}")
async def get_opening_info(game_id: str):
    """Получение информации о дебюте текущей игры"""
    game = game_manager.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    opening_info = opening_book.identify_opening(game['move_history'])
    
    return {
        "success": True,
        "opening": opening_info
    }

@app.get("/api/opening-stats/{player_name}")
async def get_player_opening_stats(player_name: str):
    """Статистика использования дебютов игроком"""
    player_games = game_history.get_player_games(player_name, limit=100)
    
    if not player_games:
        return {
            "player": player_name,
            "stats": {
                "most_played": [],
                "total_unique_openings": 0
            }
        }
    
    stats = opening_book.get_opening_stats(player_name, player_games)
    
    return {
        "player": player_name,
        "stats": stats
    }

@app.post("/api/chat/{game_id}")
async def send_chat_message(game_id: str, player_name: str, message: str):
    """Отправка сообщения в чат"""
    game = game_manager.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    # Фильтрация сообщения (максимум 200 символов)
    message = message.strip()[:200]
    
    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    chat_message = game_manager.add_chat_message(game_id, player_name, message)
    
    # Отправка всем подключенным клиентам через WebSocket
    if game_id in game_manager.connections:
        for connection in game_manager.connections[game_id]:
            try:
                await connection.send_json({
                    'type': 'chat',
                    'data': chat_message
                })
            except:
                pass
    
    return {
        "success": True,
        "message": chat_message
    }

@app.get("/api/chat/{game_id}")
async def get_chat_messages(game_id: str, limit: int = 50):
    """Получение истории чата"""
    game = game_manager.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    messages = game_manager.get_chat_history(game_id, limit)
    
    return {
        "success": True,
        "messages": messages,
        "total": len(messages)
    }

# Мультиплеер API
@app.post("/api/matchmaking/join")
async def join_matchmaking(player_name: str, rating: int = 1000, time_control: int = 0):
    """Присоединение к поиску игры"""
    player_id = game_manager.add_to_matchmaking(player_name, rating, time_control)
    return {
        "success": True,
        "player_id": player_id,
        "message": "Searching for opponent..."
    }

@app.post("/api/matchmaking/leave")
async def leave_matchmaking(player_id: str):
    """Выход из поиска игры"""
    game_manager.remove_from_matchmaking(player_id)
    return {
        "success": True,
        "message": "Left matchmaking queue"
    }

@app.get("/api/matchmaking/find/{player_id}")
async def find_match_endpoint(player_id: str):
    """Проверка найденных соперников"""
    result = game_manager.find_match(player_id)
    
    if result:
        game_id, opponent_id = result
        game = game_manager.get_game(game_id)
        return {
            "success": True,
            "match_found": True,
            "game_id": game_id,
            "white_player": game['white_player'],
            "black_player": game['black_player']
        }
    else:
        return {
            "success": True,
            "match_found": False,
            "queue_size": len(game_manager.matchmaking_queue)
        }

@app.get("/api/matchmaking/queue")
async def get_matchmaking_queue():
    """Получение состояния очереди"""
    queue_info = [{
        'player_name': p['player_name'],
        'rating': p['rating'],
        'time_control': p['time_control'],
        'waiting_time': (datetime.now() - p['joined_at']).total_seconds()
    } for p in game_manager.matchmaking_queue]
    
    return {
        "queue_size": len(game_manager.matchmaking_queue),
        "players": queue_info
    }

@app.post("/api/lobby/create")
async def create_lobby_endpoint(host_name: str, lobby_name: str, time_control: int = 0, is_private: bool = False):
    """Создание игрового лобби"""
    lobby_id = game_manager.create_lobby(host_name, lobby_name, time_control, is_private)
    return {
        "success": True,
        "lobby_id": lobby_id,
        "message": f"Lobby '{lobby_name}' created"
    }

@app.post("/api/lobby/join/{lobby_id}")
async def join_lobby_endpoint(lobby_id: str, player_name: str):
    """Присоединение к лобби"""
    success = game_manager.join_lobby(lobby_id, player_name)
    
    if success:
        return {
            "success": True,
            "message": f"Joined lobby {lobby_id}"
        }
    else:
        raise HTTPException(status_code=400, detail="Failed to join lobby")

@app.post("/api/lobby/start/{lobby_id}")
async def start_lobby_game_endpoint(lobby_id: str):
    """Запуск игры из лобби"""
    game_id = game_manager.start_lobby_game(lobby_id)
    
    if game_id:
        game = game_manager.get_game(game_id)
        return {
            "success": True,
            "game_id": game_id,
            "white_player": game['white_player'],
            "black_player": game['black_player']
        }
    else:
        raise HTTPException(status_code=400, detail="Failed to start game")

@app.get("/api/lobby/list")
async def list_lobbies():
    """Получение списка доступных лобби"""
    lobbies = game_manager.get_public_lobbies()
    return {
        "success": True,
        "lobbies": lobbies,
        "total": len(lobbies)
    }

@app.get("/api/lobby/{lobby_id}")
async def get_lobby_info(lobby_id: str):
    """Получение информации о лобби"""
    if lobby_id not in game_manager.lobbies:
        raise HTTPException(status_code=404, detail="Lobby not found")
    
    lobby = game_manager.lobbies[lobby_id]
    return {
        "success": True,
        "lobby": {
            'lobby_id': lobby['lobby_id'],
            'lobby_name': lobby['lobby_name'],
            'host': lobby['host'],
            'guest': lobby['guest'],
            'status': lobby['status'],
            'time_control': lobby['time_control']
        }
    }

@app.get("/api/profile/{player_name}")
async def get_player_profile(player_name: str):
    """Получение профиля игрока с детальной статистикой"""
    profile = profile_manager.get_or_create_profile(player_name)
    return {
        "success": True,
        "profile": profile.get_detailed_stats()
    }

@app.get("/api/profile/{player_name}/summary")
async def get_player_profile_summary(player_name: str):
    """Получение краткой статистики профиля"""
    profile = profile_manager.get_or_create_profile(player_name)
    return {
        "success": True,
        "profile": profile.get_stats_summary()
    }

@app.get("/api/profile/{player_name}/achievements")
async def get_player_achievements(player_name: str):
    """Получение достижений игрока"""
    profile = profile_manager.get_or_create_profile(player_name)
    return {
        "success": True,
        "achievements": profile.achievements,
        "total": len(profile.achievements)
    }

@app.get("/api/leaderboard/profiles")
async def get_profiles_leaderboard(sort_by: str = 'win_rate', limit: int = 10):
    """Таблица лидеров по профилям"""
    leaderboard = profile_manager.get_leaderboard(sort_by, limit)
    return {
        "success": True,
        "leaderboard": leaderboard,
        "sort_by": sort_by
    }

@app.get("/api/profile/{player_name}/opening-stats")
async def get_player_opening_stats(player_name: str):
    """Статистика дебютов игрока"""
    profile = profile_manager.get_or_create_profile(player_name)
    top_openings = profile._get_top_openings(10)
    return {
        "success": True,
        "player": player_name,
        "openings": top_openings,
        "favorite_opening": profile.favorite_opening
    }

@app.get("/api/profile/{player_name}/compare/{opponent_name}")
async def compare_profiles(player_name: str, opponent_name: str):
    """Сравнение двух профилей"""
    profile1 = profile_manager.get_or_create_profile(player_name)
    profile2 = profile_manager.get_or_create_profile(opponent_name)
    
    stats1 = profile1.get_stats_summary()
    stats2 = profile2.get_stats_summary()
    
    return {
        "success": True,
        "player1": stats1,
        "player2": stats2,
        "comparison": {
            "win_rate_diff": stats1['win_rate'] - stats2['win_rate'],
            "games_diff": stats1['games_played'] - stats2['games_played'],
            "best_streak_diff": stats1['best_win_streak'] - stats2['best_win_streak']
        }
    }

# Вспомогательные функции анализа позиции
def analyze_material(board_state: List[List[str]]) -> Dict:
    """Анализ материального баланса"""
    piece_values = {'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': 0}
    white_material = 0
    black_material = 0
    white_pieces = {'p': 0, 'n': 0, 'b': 0, 'r': 0, 'q': 0}
    black_pieces = {'p': 0, 'n': 0, 'b': 0, 'r': 0, 'q': 0}
    
    for row in board_state:
        for piece in row:
            if piece != '.':
                piece_lower = piece.lower()
                if piece.isupper():
                    white_material += piece_values.get(piece_lower, 0)
                    if piece_lower in white_pieces:
                        white_pieces[piece_lower] += 1
                else:
                    black_material += piece_values.get(piece_lower, 0)
                    if piece_lower in black_pieces:
                        black_pieces[piece_lower] += 1
    
    advantage = white_material - black_material
    
    return {
        'white_material': white_material,
        'black_material': black_material,
        'advantage': advantage,
        'advantage_side': 'white' if advantage > 0 else 'black' if advantage < 0 else 'equal',
        'white_pieces': white_pieces,
        'black_pieces': black_pieces
    }

def analyze_center_control(board_state: List[List[str]]) -> Dict:
    """Анализ контроля центра доски"""
    center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]  # d4, e4, d5, e5
    extended_center = [(2, 2), (2, 3), (2, 4), (2, 5), (3, 2), (3, 5), (4, 2), (4, 5), (5, 2), (5, 3), (5, 4), (5, 5)]
    
    white_center = 0
    black_center = 0
    
    for row, col in center_squares:
        piece = board_state[row][col]
        if piece != '.':
            if piece.isupper():
                white_center += 2
            else:
                black_center += 2
    
    for row, col in extended_center:
        piece = board_state[row][col]
        if piece != '.':
            if piece.isupper():
                white_center += 1
            else:
                black_center += 1
    
    return {
        'white_control': white_center,
        'black_control': black_center,
        'advantage': 'white' if white_center > black_center else 'black' if black_center > white_center else 'equal'
    }

def find_tactical_motifs(board_state: List[List[str]], current_turn: bool, engine) -> List[Dict]:
    """Поиск тактических мотивов (вилки, связки, открытые атаки)"""
    motifs = []
    
    # Проверка на возможные вилки конем
    for row in range(8):
        for col in range(8):
            piece = board_state[row][col]
            if piece.lower() == 'n' and piece.isupper() == current_turn:
                # Проверяем все возможные ходы коня
                knight_moves = [(row+2, col+1), (row+2, col-1), (row-2, col+1), (row-2, col-1),
                               (row+1, col+2), (row+1, col-2), (row-1, col+2), (row-1, col-2)]
                
                for to_row, to_col in knight_moves:
                    if 0 <= to_row < 8 and 0 <= to_col < 8:
                        target = board_state[to_row][to_col]
                        if target != '.' and target.isupper() != current_turn:
                            # Проверяем, атакует ли конь с этой позиции другие ценные фигуры
                            attacked_pieces = 0
                            for check_row, check_col in knight_moves:
                                adj_row = to_row + (check_row - row)
                                adj_col = to_col + (check_col - col)
                                if 0 <= adj_row < 8 and 0 <= adj_col < 8:
                                    check_piece = board_state[adj_row][adj_col]
                                    if check_piece != '.' and check_piece.isupper() != current_turn and check_piece.lower() in ['r', 'q', 'k']:
                                        attacked_pieces += 1
                            
                            if attacked_pieces >= 2:
                                motifs.append({
                                    'type': 'fork',
                                    'piece': 'knight',
                                    'from': (row, col),
                                    'to': (to_row, to_col),
                                    'targets': attacked_pieces
                                })
    
    # Проверка на возможные связки
    for row in range(8):
        for col in range(8):
            piece = board_state[row][col]
            if piece != '.' and piece.isupper() == current_turn:
                piece_type = piece.lower()
                if piece_type in ['b', 'r', 'q']:
                    # Проверка линий атаки
                    directions = []
                    if piece_type in ['r', 'q']:
                        directions.extend([(0, 1), (0, -1), (1, 0), (-1, 0)])
                    if piece_type in ['b', 'q']:
                        directions.extend([(1, 1), (1, -1), (-1, 1), (-1, -1)])
                    
                    for dr, dc in directions:
                        pinned_piece = None
                        target_piece = None
                        r, c = row + dr, col + dc
                        
                        while 0 <= r < 8 and 0 <= c < 8:
                            current_piece = board_state[r][c]
                            if current_piece != '.':
                                if pinned_piece is None:
                                    if current_piece.isupper() != current_turn:
                                        pinned_piece = (r, c, current_piece)
                                    else:
                                        break
                                else:
                                    if current_piece.isupper() != current_turn and current_piece.lower() in ['k', 'q', 'r']:
                                        target_piece = (r, c, current_piece)
                                        motifs.append({
                                            'type': 'pin',
                                            'piece': piece_type,
                                            'attacker': (row, col),
                                            'pinned': pinned_piece[:2],
                                            'target': target_piece[:2]
                                        })
                                    break
                            r += dr
                            c += dc
    
    return motifs

def analyze_king_safety(board_state: List[List[str]], current_turn: bool, engine) -> Dict:
    """Анализ безопасности королей"""
    def find_king(is_white: bool) -> tuple:
        king = 'K' if is_white else 'k'
        for row in range(8):
            for col in range(8):
                if board_state[row][col] == king:
                    return (row, col)
        return None
    
    def count_defenders(king_pos: tuple, is_white: bool) -> int:
        row, col = king_pos
        defenders = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    piece = board_state[r][c]
                    if piece != '.' and piece.isupper() == is_white:
                        defenders += 1
        return defenders
    
    white_king_pos = find_king(True)
    black_king_pos = find_king(False)
    
    white_safety = {
        'position': white_king_pos,
        'defenders': count_defenders(white_king_pos, True) if white_king_pos else 0,
        'in_check': engine.is_king_in_check(True) if hasattr(engine, 'is_king_in_check') else False,
        'castled': white_king_pos[1] in [2, 6] if white_king_pos else False
    }
    
    black_safety = {
        'position': black_king_pos,
        'defenders': count_defenders(black_king_pos, False) if black_king_pos else 0,
        'in_check': engine.is_king_in_check(False) if hasattr(engine, 'is_king_in_check') else False,
        'castled': black_king_pos[1] in [2, 6] if black_king_pos else False
    }
    
    return {
        'white': white_safety,
        'black': black_safety
    }

def analyze_pawn_structure(board_state: List[List[str]]) -> Dict:
    """Анализ пешечной структуры"""
    white_pawns = []
    black_pawns = []
    
    for row in range(8):
        for col in range(8):
            piece = board_state[row][col]
            if piece == 'P':
                white_pawns.append((row, col))
            elif piece == 'p':
                black_pawns.append((row, col))
    
    def count_doubled_pawns(pawns):
        columns = {}
        for _, col in pawns:
            columns[col] = columns.get(col, 0) + 1
        return sum(1 for count in columns.values() if count > 1)
    
    def count_isolated_pawns(pawns):
        columns = set(col for _, col in pawns)
        isolated = 0
        for _, col in pawns:
            if (col - 1) not in columns and (col + 1) not in columns:
                isolated += 1
        return isolated
    
    def count_passed_pawns(own_pawns, opponent_pawns, is_white):
        passed = 0
        for row, col in own_pawns:
            has_blocker = False
            direction = -1 if is_white else 1
            check_row = row + direction
            
            while 0 <= check_row < 8:
                for check_col in [col - 1, col, col + 1]:
                    if 0 <= check_col < 8 and (check_row, check_col) in opponent_pawns:
                        has_blocker = True
                        break
                if has_blocker:
                    break
                check_row += direction
            
            if not has_blocker:
                passed += 1
        return passed
    
    return {
        'white': {
            'total': len(white_pawns),
            'doubled': count_doubled_pawns(white_pawns),
            'isolated': count_isolated_pawns(white_pawns),
            'passed': count_passed_pawns(white_pawns, black_pawns, True)
        },
        'black': {
            'total': len(black_pawns),
            'doubled': count_doubled_pawns(black_pawns),
            'isolated': count_isolated_pawns(black_pawns),
            'passed': count_passed_pawns(black_pawns, white_pawns, False)
        }
    }

def get_top_moves(engine, board_state: List[List[str]], current_turn: bool, depth: int, top_n: int = 3) -> List[Dict]:
    """Получение топ N лучших ходов"""
    moves = []
    
    try:
        # Генерация всех возможных ходов
        possible_moves = []
        for from_row in range(8):
            for from_col in range(8):
                piece = board_state[from_row][from_col]
                if piece != '.' and piece.isupper() == current_turn:
                    for to_row in range(8):
                        for to_col in range(8):
                            if hasattr(engine, 'is_valid_move') and engine.is_valid_move((from_row, from_col), (to_row, to_col)):
                                possible_moves.append(((from_row, from_col), (to_row, to_col)))
        
        # Оценка каждого хода
        move_scores = []
        for move in possible_moves[:50]:  # Ограничиваем для производительности
            # Простая эвристическая оценка
            from_pos, to_pos = move
            target = board_state[to_pos[0]][to_pos[1]]
            score = 0
            
            if target != '.':
                piece_values = {'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9}
                score += piece_values.get(target.lower(), 0) * 10
            
            # Бонус за контроль центра
            if to_pos in [(3, 3), (3, 4), (4, 3), (4, 4)]:
                score += 5
            
            move_scores.append((move, score))
        
        # Сортировка и выбор топ N
        move_scores.sort(key=lambda x: x[1], reverse=True)
        
        for (from_pos, to_pos), score in move_scores[:top_n]:
            piece = board_state[from_pos[0]][from_pos[1]]
            moves.append({
                'from': from_pos,
                'to': to_pos,
                'piece': piece,
                'score': score,
                'notation': f"{chr(97 + from_pos[1])}{8 - from_pos[0]}-{chr(97 + to_pos[1])}{8 - to_pos[0]}"
            })
    
    except Exception as e:
        logger.error(f"Error getting top moves: {e}")
    
    return moves

def evaluate_position(board_state: List[List[str]], current_turn: bool) -> Dict:
    """Общая оценка позиции"""
    material = analyze_material(board_state)
    center = analyze_center_control(board_state)
    
    # Простая оценка в сантипешках
    score = material['advantage'] * 100
    
    # Бонус за контроль центра
    if center['advantage'] == 'white':
        score += 20
    elif center['advantage'] == 'black':
        score -= 20
    
    # Определение оценки
    if abs(score) < 50:
        evaluation = "равная позиция"
    elif score > 0:
        evaluation = f"преимущество белых (+{abs(score/100):.1f})"
    else:
        evaluation = f"преимущество черных (-{abs(score/100):.1f})"
    
    return {
        'score': score,
        'evaluation': evaluation,
        'side_to_move': 'white' if current_turn else 'black'
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")