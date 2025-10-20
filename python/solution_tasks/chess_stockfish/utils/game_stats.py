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
from typing import List, Dict, Optional


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
                # Если файл поврежден, создаем новый
                return {'games': [], 'total_wins': 0, 'total_losses': 0, 'total_draws': 0}
        return {'games': [], 'total_wins': 0, 'total_losses': 0, 'total_draws': 0}
    
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
            'result': game_stats['game_reason'] or 'Неизвестно',
            'fen': game_stats['fen']
        }
        
        self.stats['games'].append(game_record)
        
        # Обновить счёт побед/поражений/ничьих
        if game_stats['game_reason']:
            if 'Победили' in game_stats['game_reason']:
                if f"Победили {game_stats['player_color']}" in game_stats['game_reason']:
                    self.stats['total_wins'] += 1
                else:
                    self.stats['total_losses'] += 1
            elif 'Пат' in game_stats['game_reason'] or 'Ничья' in game_stats['game_reason']:
                self.stats['total_draws'] += 1
            else:
                # Other result, count as loss
                self.stats['total_losses'] += 1
        else:
            # Если игра не завершена, считаем поражением
            self.stats['total_losses'] += 1
        
        self._save_stats()
    
    def _save_stats(self):
        """Сохранить статистику в файл."""
        try:
            # Создаем резервную копию перед сохранением
            if os.path.exists(self.stats_file):
                backup_file = self.stats_file + '.backup'
                import shutil
                shutil.copy2(self.stats_file, backup_file)
            
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
        total_games = len(self.stats['games'])
        return {
            'total_games': total_games,
            'total_wins': self.stats['total_wins'],
            'total_losses': self.stats['total_losses'],
            'total_draws': self.stats['total_draws'],
            'win_rate': (self.stats['total_wins'] / total_games * 100 if total_games > 0 else 0),
            'loss_rate': (self.stats['total_losses'] / total_games * 100 if total_games > 0 else 0),
            'draw_rate': (self.stats['total_draws'] / total_games * 100 if total_games > 0 else 0)
        }
    
    def get_games_by_color(self, color: str) -> List[Dict]:
        """
        Получить список игр за определённый цвет.
        
        Параметры:
            color (str): Цвет ('white' или 'black')
            
        Возвращает:
            List[Dict]: Список игр за указанный цвет
        """
        return [game for game in self.stats['games'] if game['player_color'] == color]
    
    def get_games_by_level(self, level: int) -> List[Dict]:
        """
        Получить список игр на определённом уровне сложности.
        
        Параметры:
            level (int): Уровень сложности (0-20)
            
        Возвращает:
            List[Dict]: Список игр на указанном уровне
        """
        return [game for game in self.stats['games'] if game['skill_level'] == level]
    
    def get_recent_games(self, count: int = 10) -> List[Dict]:
        """
        Получить последние игры.
        
        Параметры:
            count (int): Количество последних игр
            
        Возвращает:
            List[Dict]: Список последних игр
        """
        # Сортируем по времени и возвращаем последние count игр
        sorted_games = sorted(self.stats['games'], key=lambda x: x['timestamp'], reverse=True)
        return sorted_games[:count]
    
    def get_best_performance(self) -> Optional[Dict]:
        """
        Получить игру с лучшим результатом (наибольшее количество ходов).
        
        Возвращает:
            Dict: Игра с наибольшим количеством ходов или None
        """
        if not self.stats['games']:
            return None
        
        # Проверяем, что список не пустой
        if len(self.stats['games']) == 0:
            return None
            
        try:
            return max(self.stats['games'], key=lambda x: x['total_moves'] if isinstance(x, dict) and 'total_moves' in x else 0)
        except ValueError:
            return None
    
    def get_level_performance(self) -> Dict[int, Dict]:
        """
        Получить статистику по уровням сложности.
        
        Возвращает:
            Dict[int, Dict]: Словарь с статистикой по каждому уровню
        """
        level_stats = {}
        
        for game in self.stats['games']:
            level = game['skill_level']
            if level not in level_stats:
                level_stats[level] = {'wins': 0, 'losses': 0, 'draws': 0, 'total': 0, 'moves': 0}
            
            level_stats[level]['total'] += 1
            level_stats[level]['moves'] += game['total_moves']
            
            if game['result'] and 'Победили' in str(game['result']):
                if f"Победили {game['player_color']}" in str(game['result']):
                    level_stats[level]['wins'] += 1
                else:
                    level_stats[level]['losses'] += 1
            elif game['result'] and ('Пат' in str(game['result']) or 'Ничья' in str(game['result'])):
                level_stats[level]['draws'] += 1
            else:
                level_stats[level]['losses'] += 1
        
        # Вычисляем проценты
        for level in level_stats:
            total = level_stats[level]['total']
            if total > 0:
                level_stats[level]['win_rate'] = level_stats[level]['wins'] / total * 100
                level_stats[level]['avg_moves'] = level_stats[level]['moves'] / total
            else:
                level_stats[level]['win_rate'] = 0
                level_stats[level]['avg_moves'] = 0
        
        return level_stats
    
    def clear_stats(self):
        """Очистить всю статистику."""
        self.stats = {'games': [], 'total_wins': 0, 'total_losses': 0, 'total_draws': 0}
        self._save_stats()
        print("📊 Статистика очищена")