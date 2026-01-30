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
    
    def create_game(self, player_name: str = "Anonymous", game_mode: str = "ai", time_control: int = 0) -> str:
        game_id = str(uuid.uuid4())
        # Конвертация времени из минут в секунды
        time_per_player = time_control * 60 if time_control > 0 else 0
        
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
            "e2-e4 e7-e5 g1-f3 b8-c6 f1-c4 f8-c5": "Italian Game: Giuoco Piano",
            "e2-e4 e7-e5 g1-f3 b8-c6 d2-d4": "Scotch Game",
            "e2-e4 e7-e5 g1-f3 g8-f6": "Petrov's Defense (Russian Game)",
            "e2-e4 e7-e5 f2-f4": "King's Gambit",
            
            # Полуоткрытые дебюты
            "e2-e4 c7-c5": "Sicilian Defense",
            "e2-e4 c7-c5 g1-f3": "Sicilian Defense: Open",
            "e2-e4 c7-c5 g1-f3 d7-d6": "Sicilian Defense: Najdorf Variation",
            "e2-e4 c7-c6": "Caro-Kann Defense",
            "e2-e4 e7-e6": "French Defense",
            "e2-e4 d7-d5": "Scandinavian Defense",
            "e2-e4 g8-f6": "Alekhine's Defense",
            
            # Закрытые дебюты (1.d4 d5)
            "d2-d4 d7-d5": "Queen's Pawn Opening",
            "d2-d4 d7-d5 c2-c4": "Queen's Gambit",
            "d2-d4 d7-d5 c2-c4 d5-c4": "Queen's Gambit Accepted",
            "d2-d4 d7-d5 c2-c4 e7-e6": "Queen's Gambit Declined",
            "d2-d4 d7-d5 c2-c4 c7-c6": "Slav Defense",
            "d2-d4 g8-f6 c2-c4 e7-e6": "Indian Defense",
            "d2-d4 g8-f6 c2-c4 g7-g6": "King's Indian Defense",
            "d2-d4 g8-f6 c2-c4 e7-e6 g1-f3 b7-b6": "Queen's Indian Defense",
            
            # Индийские защиты
            "d2-d4 g8-f6": "Indian Defense",
            "d2-d4 g8-f6 c2-c4 e7-e6 g1-f3 f8-b4": "Nimzo-Indian Defense",
            "d2-d4 g8-f6 c2-c4 c7-c5": "Benoni Defense",
            
            # Фланговые дебюты
            "c2-c4": "English Opening",
            "g1-f3": "Reti Opening",
            "g2-g3": "King's Fianchetto Opening",
            "b2-b3": "Larsen's Opening",
            
            # Необычные дебюты
            "e2-e4 g7-g6": "Modern Defense",
            "e2-e4 b8-c6": "Nimzowitsch Defense",
            "f2-f4": "Bird's Opening",
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
            
            # Обновление статуса игры безопасно без вызова is_checkmate
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

# WebSocket endpoint для real-time обновлений
@app.websocket("/ws/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str):
    """WebSocket endpoint для real-time обновлений игры"""
    await websocket.accept()
    
    try:
        # Добавление подключения к игре
        if game_id in game_manager.connections:
            game_manager.connections[game_id].append(websocket)
        
        while True:
            # Поддержание соединения активным
            await asyncio.sleep(1)
            
    except WebSocketDisconnect:
        # Удаление подключения
        if game_id in game_manager.connections:
            if websocket in game_manager.connections[game_id]:
                game_manager.connections[game_id].remove(websocket)

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
    
    # Обновление статистики игрока
    player_stats.update_stats(game['player_name'], game)
    
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")