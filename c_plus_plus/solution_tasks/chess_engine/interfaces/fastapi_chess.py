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
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
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

# Подключение статических файлов
app.mount("/static", StaticFiles(directory="web"), name="static")

# Управление играми
class GameManager:
    def __init__(self):
        self.games: Dict[str, dict] = {}
        self.connections: Dict[str, List[WebSocket]] = {}
    
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
        logger.info(f"Deleted game {game_id}")

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

# Pydantic модели
class MoveRequest(BaseModel):
    game_id: str = Field(..., description="ID игры")
    from_pos: Tuple[int, int] = Field(..., description="Начальная позиция (row, col)")
    to_pos: Tuple[int, int] = Field(..., description="Конечная позиция (row, col)")
    player_color: bool = Field(..., description="Цвет игрока (True=белые, False=черные)")
    
    @validator('from_pos', 'to_pos')
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
    
    @validator('player_name')
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
                    game_mode=game['game_mode']
                )
            }
            
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")