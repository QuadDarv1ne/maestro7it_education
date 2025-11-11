"""
Модуль для отслеживания состояния приложения.
Предоставляет централизованное управление состоянием и статистикой.
"""

import threading
import time
from typing import Dict, Any
from dataclasses import dataclass
from collections import deque
import logging

logger = logging.getLogger(__name__)

@dataclass
class GameStats:
    """Статистика игры"""
    total_moves: int = 0
    total_time: float = 0.0
    avg_move_time: float = 0.0
    total_errors: int = 0
    start_time: float = 0.0

class AppState:
    """
    Класс для отслеживания состояния приложения.
    Обеспечивает thread-safe доступ к общим ресурсам.
    """
    
    def __init__(self):
        self._lock = threading.RLock()
        self._games: Dict[str, Any] = {}
        self._session_timestamps: Dict[str, float] = {}
        self._game_stats: Dict[str, GameStats] = {}
        self._active_game_count: int = 0
        self._peak_active_games: int = 0
        self._total_games_created: int = 0
        self._total_games_cleaned: int = 0
        self._resource_stats = {
            'total_games_created': 0,
            'total_games_cleaned': 0,
            'peak_active_games': 0,
            'total_sessions': 0,
            'peak_sessions': 0
        }
        self._error_history = deque(maxlen=100)  # Хранение последних 100 ошибок
        
    def add_game(self, session_id: str, game: Any) -> bool:
        """
        Добавление новой игры в отслеживание.
        
        Args:
            session_id: ID сессии
            game: Объект игры
            
        Returns:
            bool: Успешность операции
        """
        with self._lock:
            try:
                if session_id in self._games:
                    # Очистка существующей игры
                    self._remove_game(session_id)
                
                self._games[session_id] = game
                self._session_timestamps[session_id] = time.time()
                self._game_stats[session_id] = GameStats(start_time=time.time())
                self._active_game_count += 1
                self._total_games_created += 1
                
                # Обновление пиковых значений
                self._peak_active_games = max(self._peak_active_games, self._active_game_count)
                self._resource_stats['peak_active_games'] = self._peak_active_games
                self._resource_stats['total_games_created'] = self._total_games_created
                
                return True
            except Exception as e:
                logger.error(f"Error adding game for session {session_id}: {e}")
                self._error_history.append({
                    'time': time.time(),
                    'type': 'add_game',
                    'session_id': session_id,
                    'error': str(e)
                })
                return False
    
    def remove_game(self, session_id: str) -> bool:
        """
        Удаление игры из отслеживания.
        
        Args:
            session_id: ID сессии
            
        Returns:
            bool: Успешность операции
        """
        with self._lock:
            try:
                return self._remove_game(session_id)
            except Exception as e:
                logger.error(f"Error removing game for session {session_id}: {e}")
                self._error_history.append({
                    'time': time.time(),
                    'type': 'remove_game',
                    'session_id': session_id,
                    'error': str(e)
                })
                return False
    
    def _remove_game(self, session_id: str) -> bool:
        """Внутренний метод удаления игры"""
        if session_id in self._games:
            del self._games[session_id]
            self._active_game_count = max(0, self._active_game_count - 1)
            self._total_games_cleaned += 1
            self._resource_stats['total_games_cleaned'] = self._total_games_cleaned
            
            # Очистка связанных данных
            self._session_timestamps.pop(session_id, None)
            self._game_stats.pop(session_id, None)
            
            return True
        return False
    
    def get_game(self, session_id: str) -> Any:
        """
        Получение объекта игры.
        
        Args:
            session_id: ID сессии
            
        Returns:
            Any: Объект игры или None
        """
        with self._lock:
            return self._games.get(session_id)
    
    def update_game_stats(self, session_id: str, move_time: float, is_error: bool = False):
        """
        Обновление статистики игры.
        
        Args:
            session_id: ID сессии
            move_time: Время выполнения хода
            is_error: Флаг ошибки
        """
        with self._lock:
            if session_id in self._game_stats:
                stats = self._game_stats[session_id]
                stats.total_moves += 1
                stats.total_time += move_time
                stats.avg_move_time = stats.total_time / stats.total_moves
                if is_error:
                    stats.total_errors += 1
    
    def get_stale_sessions(self, timeout: float) -> list:
        """
        Получение списка устаревших сессий.
        
        Args:
            timeout: Время неактивности в секундах
            
        Returns:
            list: Список ID устаревших сессий
        """
        with self._lock:
            current_time = time.time()
            return [
                session_id for session_id, timestamp in self._session_timestamps.items()
                if current_time - timestamp > timeout
            ]
    
    def get_stats(self) -> dict:
        """
        Получение статистики состояния.
        
        Returns:
            dict: Статистика приложения
        """
        with self._lock:
            return {
                'active_games': self._active_game_count,
                'peak_active_games': self._peak_active_games,
                'total_games_created': self._total_games_created,
                'total_games_cleaned': self._total_games_cleaned,
                'tracked_sessions': len(self._session_timestamps),
                'game_stats': {
                    session_id: {
                        'total_moves': stats.total_moves,
                        'avg_move_time': stats.avg_move_time,
                        'total_errors': stats.total_errors,
                        'duration': time.time() - stats.start_time
                    }
                    for session_id, stats in self._game_stats.items()
                },
                'resource_stats': self._resource_stats.copy(),
                'recent_errors': list(self._error_history)
            }
    
    def reset_stats(self):
        """Сброс статистики"""
        with self._lock:
            self._total_games_created = 0
            self._total_games_cleaned = 0
            self._peak_active_games = self._active_game_count
            self._resource_stats = {
                'total_games_created': 0,
                'total_games_cleaned': 0,
                'peak_active_games': self._active_game_count,
                'total_sessions': len(self._session_timestamps),
                'peak_sessions': len(self._session_timestamps)
            }
            self._error_history.clear()

# Глобальный экземпляр для отслеживания состояния
app_state = AppState()