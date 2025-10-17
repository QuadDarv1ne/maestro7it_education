# ============================================================================
# utils/game_stats.py
# ============================================================================

"""
Модуль: utils/game_stats.py

Описание:
    Содержит утилиты для сохранения и анализа статистики игр.
    Позволяет:
    - Сохранять результаты игр
    - Анализировать прогресс
    - Экспортировать игры в PGN
    
Возможности:
    - Накопление статистики
    - Анализ побед/поражений
    - Экспорт в стандартные форматы
"""

import json
from datetime import datetime
import os


class GameStatistics:
    """
    Класс для управления статистикой игр.
    
    Сохраняет информацию о сыгранных партиях для дальнейшего анализа.
    """
    
    def __init__(self, stats_file: str = 'game_stats.json'):
        """
        Инициализация статистики.
        
        Параметры:
            stats_file (str): Путь к файлу со статистикой
        """
        self.stats_file = stats_file
        self.stats = self._load_stats()
    
    def _load_stats(self) -> dict:
        """
        Загрузить статистику из файла.
        
        Возвращает:
            dict: Словарь со статистикой или пустой словарь если файла нет
        """
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {'games': [], 'total_wins': 0, 'total_losses': 0}
        return {'games': [], 'total_wins': 0, 'total_losses': 0}
    
    def save_game(self, game_stats: dict):
        """
        Сохранить информацию об игре.
        
        Параметры:
            game_stats (dict): Статистика игры от ChessGame.get_game_stats()
        """
        game_record = {
            'timestamp': datetime.now().isoformat(),
            'player_color': game_stats['player_color'],
            'skill_level': game_stats['skill_level'],
            'total_moves': game_stats['total_moves'],
            'result': game_stats['game_reason'],
            'fen': game_stats['fen']
        }
        
        self.stats['games'].append(game_record)
        
        # Обновить счёт побед/поражений
        if 'Победили' in str(game_stats['game_reason']):
            self.stats['total_wins'] += 1
        else:
            self.stats['total_losses'] += 1
        
        self._save_stats()
    
    def _save_stats(self):
        """Сохранить статистику в файл."""
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️  Ошибка при сохранении статистики: {e}")
    
    def get_summary(self) -> dict:
        """
        Получить сводку по статистике.
        
        Возвращает:
            dict: Общая статистика по всем играм
        """
        return {
            'total_games': len(self.stats['games']),
            'total_wins': self.stats['total_wins'],
            'total_losses': self.stats['total_losses'],
            'win_rate': (self.stats['total_wins'] / len(self.stats['games']) * 100 
                        if self.stats['games'] else 0)
        }