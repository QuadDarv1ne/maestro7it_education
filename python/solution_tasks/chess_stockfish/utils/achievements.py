# ============================================================================
# utils/achievements.py
# ============================================================================

"""
Модуль: utils/achievements.py

Описание:
    Содержит реализацию системы достижений для шахматной игры chess_stockfish.
    Предоставляет систему наград за образовательные и игровые достижения.
    
Возможности:
    - Достижения за изучение дебютов
    - Достижения за освоение эндшпилей
    - Достижения за игровые успехи
    - Система уровней и рейтинга
"""

from typing import Dict, List, Optional, Set
import json
import os

# Определение достижений
ACHIEVEMENTS = {
    # Образовательные достижения
    "first_lesson": {
        "name": "Первый урок",
        "description": "Получите первую образовательную подсказку",
        "category": "education",
        "points": 10,
        "icon": "🎓"
    },
    "openings_student": {
        "name": "Студент дебютов",
        "description": "Изучите 5 различных дебютов",
        "category": "education",
        "points": 50,
        "icon": "📚"
    },
    "openings_master": {
        "name": "Мастер дебютов",
        "description": "Изучите 15 различных дебютов",
        "category": "education",
        "points": 150,
        "icon": "📖"
    },
    "endgame_student": {
        "name": "Студент эндшпилей",
        "description": "Завершите 5 эндшпильных сценариев",
        "category": "education",
        "points": 50,
        "icon": "🏁"
    },
    "endgame_master": {
        "name": "Мастер эндшпилей",
        "description": "Завершите 15 эндшпильных сценариев",
        "category": "education",
        "points": 150,
        "icon": "♛"
    },
    "knowledge_seeker": {
        "name": "Искатель знаний",
        "description": "Получите 50 образовательных подсказок",
        "category": "education",
        "points": 100,
        "icon": "💡"
    },
    "strategy_master": {
        "name": "Мастер стратегии",
        "description": "Получите 200 образовательных подсказок",
        "category": "education",
        "points": 300,
        "icon": "🧠"
    },
    
    # Игровые достижения
    "first_game": {
        "name": "Первая игра",
        "description": "Сыграйте свою первую партию",
        "category": "gameplay",
        "points": 20,
        "icon": "♟️"
    },
    "victory": {
        "name": "Победа!",
        "description": "Выиграйте свою первую партию",
        "category": "gameplay",
        "points": 50,
        "icon": "🏆"
    },
    "checkmate_master": {
        "name": "Мастер мата",
        "description": "Поставьте мат 10 раз",
        "category": "gameplay",
        "points": 100,
        "icon": "🪓"
    },
    "draw_master": {
        "name": "Мастер ничьих",
        "description": "Сыграйте 20 ничьих",
        "category": "gameplay",
        "points": 75,
        "icon": "🤝"
    },
    "moves_master": {
        "name": "Мастер ходов",
        "description": "Сделайте 1000 ходов",
        "category": "gameplay",
        "points": 150,
        "icon": "🔢"
    },
    "captures_master": {
        "name": "Мастер захвата",
        "description": "Сделайте 100 взятий",
        "category": "gameplay",
        "points": 120,
        "icon": "⚔️"
    },
    "time_master": {
        "name": "Мастер времени",
        "description": "Сыграйте 10 часов",
        "category": "gameplay",
        "points": 200,
        "icon": "⏰"
    },
    
    # Специальные достижения
    "perfect_game": {
        "name": "Идеальная игра",
        "description": "Выиграйте партию без потерь фигур",
        "category": "special",
        "points": 200,
        "icon": "⭐"
    },
    "comeback_king": {
        "name": "Король возвращения",
        "description": "Выиграйте партию после проигрыша более 5 очков",
        "category": "special",
        "points": 150,
        "icon": "🔥"
    },
    "speed_demon": {
        "name": "Скоростной демон",
        "description": "Выиграйте партию менее чем за 10 ходов",
        "category": "special",
        "points": 100,
        "icon": "⚡"
    },
    "patience_master": {
        "name": "Мастер терпения",
        "description": "Сыграйте партию более 100 ходов",
        "category": "special",
        "points": 75,
        "icon": "🐢"
    }
}

# Награды за уровни
LEVELS = {
    1: {"name": "Новичок", "points_required": 0, "icon": "🌱"},
    2: {"name": "Ученик", "points_required": 100, "icon": "📚"},
    3: {"name": "Студент", "points_required": 300, "icon": "🎓"},
    4: {"name": "Эксперт", "points_required": 600, "icon": "🔬"},
    5: {"name": "Мастер", "points_required": 1000, "icon": "👑"},
    6: {"name": "Гроссмейстер", "points_required": 1500, "icon": "🏆"},
    7: {"name": "Легенда", "points_required": 2500, "icon": "🌟"}
}

class AchievementSystem:
    """
    Система достижений для шахматной игры.
    """
    
    def __init__(self, save_file: str = "achievements.json"):
        self.save_file = save_file
        self.achievements = {}  # Полученные достижения
        self.stats = {
            "educational_hints": 0,
            "openings_learned": set(),
            "endgames_completed": 0,
            "games_played": 0,
            "games_won": 0,
            "checkmates": 0,
            "draws": 0,
            "moves_made": 0,
            "captures": 0,
            "time_played": 0,  # в секундах
            "perfect_games": 0,
            "comeback_wins": 0,
            "short_games": 0,  # менее 10 ходов
            "long_games": 0    # более 100 ходов
        }
        self.total_points = 0
        self.level = 1
        self.unlocked_achievements = set()
        self.new_achievements = []  # Недавно полученные достижения
        
        # Загружаем сохраненные достижения
        self.load_achievements()
    
    def load_achievements(self):
        """Загрузить сохраненные достижения из файла."""
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.achievements = data.get('achievements', {})
                    self.stats = data.get('stats', self.stats)
                    # Конвертируем список в множество для openings_learned
                    if 'openings_learned' in self.stats:
                        self.stats['openings_learned'] = set(self.stats['openings_learned'])
                    self.total_points = data.get('total_points', 0)
                    self.level = data.get('level', 1)
                    self.unlocked_achievements = set(data.get('unlocked_achievements', []))
        except Exception as e:
            print(f"Ошибка загрузки достижений: {e}")
    
    def save_achievements(self):
        """Сохранить достижения в файл."""
        try:
            # Конвертируем множество в список для сериализации
            stats_to_save = self.stats.copy()
            if 'openings_learned' in stats_to_save:
                stats_to_save['openings_learned'] = list(stats_to_save['openings_learned'])
            
            data = {
                'achievements': self.achievements,
                'stats': stats_to_save,
                'total_points': self.total_points,
                'level': self.level,
                'unlocked_achievements': list(self.unlocked_achievements)
            }
            
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения достижений: {e}")
    
    def get_achievement_info(self, achievement_id: str) -> Optional[Dict]:
        """
        Получить информацию о достижении.
        
        Параметры:
            achievement_id (str): Идентификатор достижения
            
        Возвращает:
            Dict: Информация о достижении или None
        """
        return ACHIEVEMENTS.get(achievement_id)
    
    def get_all_achievements(self) -> Dict:
        """
        Получить все достижения.
        
        Возвращает:
            Dict: Все достижения
        """
        return ACHIEVEMENTS.copy()
    
    def get_unlocked_achievements(self) -> List[Dict]:
        """
        Получить список полученных достижений.
        
        Возвращает:
            List[Dict]: Список полученных достижений
        """
        unlocked = []
        for achievement_id in self.unlocked_achievements:
            info = self.get_achievement_info(achievement_id)
            if info:
                unlocked.append({
                    "id": achievement_id,
                    "info": info,
                    "unlocked_at": self.achievements.get(achievement_id)
                })
        return unlocked
    
    def get_locked_achievements(self) -> List[Dict]:
        """
        Получить список неполученных достижений.
        
        Возвращает:
            List[Dict]: Список неполученных достижений
        """
        locked = []
        for achievement_id, info in ACHIEVEMENTS.items():
            if achievement_id not in self.unlocked_achievements:
                locked.append({
                    "id": achievement_id,
                    "info": info
                })
        return locked
    
    def check_achievements(self) -> List[str]:
        """
        Проверить, какие достижения были разблокированы.
        
        Возвращает:
            List[str]: Список ID новых достижений
        """
        new_achievements = []
        
        # Проверяем все достижения
        for achievement_id, info in ACHIEVEMENTS.items():
            if achievement_id not in self.unlocked_achievements:
                unlocked = False
                
                # Проверяем условия в зависимости от категории
                if achievement_id == "first_lesson":
                    unlocked = self.stats["educational_hints"] >= 1
                elif achievement_id == "openings_student":
                    unlocked = len(self.stats["openings_learned"]) >= 5
                elif achievement_id == "openings_master":
                    unlocked = len(self.stats["openings_learned"]) >= 15
                elif achievement_id == "endgame_student":
                    unlocked = self.stats["endgames_completed"] >= 5
                elif achievement_id == "endgame_master":
                    unlocked = self.stats["endgames_completed"] >= 15
                elif achievement_id == "knowledge_seeker":
                    unlocked = self.stats["educational_hints"] >= 50
                elif achievement_id == "strategy_master":
                    unlocked = self.stats["educational_hints"] >= 200
                elif achievement_id == "first_game":
                    unlocked = self.stats["games_played"] >= 1
                elif achievement_id == "victory":
                    unlocked = self.stats["games_won"] >= 1
                elif achievement_id == "checkmate_master":
                    unlocked = self.stats["checkmates"] >= 10
                elif achievement_id == "draw_master":
                    unlocked = self.stats["draws"] >= 20
                elif achievement_id == "moves_master":
                    unlocked = self.stats["moves_made"] >= 1000
                elif achievement_id == "captures_master":
                    unlocked = self.stats["captures"] >= 100
                elif achievement_id == "time_master":
                    unlocked = self.stats["time_played"] >= 36000  # 10 часов
                elif achievement_id == "perfect_game":
                    unlocked = self.stats["perfect_games"] >= 1
                elif achievement_id == "comeback_king":
                    unlocked = self.stats["comeback_wins"] >= 1
                elif achievement_id == "speed_demon":
                    unlocked = self.stats["short_games"] >= 1
                elif achievement_id == "patience_master":
                    unlocked = self.stats["long_games"] >= 1
                
                # Если достижение разблокировано
                if unlocked:
                    import time
                    self.achievements[achievement_id] = time.time()
                    self.unlocked_achievements.add(achievement_id)
                    self.total_points += info["points"]
                    new_achievements.append(achievement_id)
                    self.new_achievements.append(achievement_id)
        
        # Проверяем уровень
        old_level = self.level
        self.level = self.calculate_level()
        
        # Если уровень повысился, добавляем это как достижение
        if self.level > old_level:
            self.new_achievements.append(f"level_up_{self.level}")
        
        # Сохраняем изменения
        if new_achievements:
            self.save_achievements()
        
        return new_achievements
    
    def calculate_level(self) -> int:
        """
        Рассчитать текущий уровень.
        
        Возвращает:
            int: Текущий уровень
        """
        for level_num in sorted(LEVELS.keys(), reverse=True):
            if self.total_points >= LEVELS[level_num]["points_required"]:
                return level_num
        return 1
    
    def get_level_info(self, level: Optional[int] = None) -> Optional[Dict]:
        """
        Получить информацию об уровне.
        
        Параметры:
            level (int): Номер уровня (по умолчанию текущий)
            
        Возвращает:
            Dict: Информация об уровне или None
        """
        if level is None:
            level = self.level
        return LEVELS.get(level)
    
    def get_progress_to_next_level(self) -> Tuple[int, int, int]:
        """
        Получить прогресс до следующего уровня.
        
        Возвращает:
            Tuple[int, int, int]: (текущие очки, очки до следующего уровня, процент)
        """
        current_level_info = self.get_level_info(self.level)
        next_level_info = self.get_level_info(self.level + 1)
        
        if not current_level_info:
            return (0, 0, 0)
        
        current_points = self.total_points - current_level_info["points_required"]
        
        if not next_level_info:
            # Максимальный уровень
            return (current_points, 0, 100)
        
        points_needed = next_level_info["points_required"] - current_level_info["points_required"]
        progress_percent = int((current_points / points_needed) * 100) if points_needed > 0 else 100
        
        return (current_points, points_needed, progress_percent)
    
    def get_new_achievements(self) -> List[Dict]:
        """
        Получить список недавно полученных достижений.
        
        Возвращает:
            List[Dict]: Список недавно полученных достижений
        """
        new_achievements = []
        for achievement_id in self.new_achievements:
            if achievement_id.startswith("level_up_"):
                # Специальная обработка для повышения уровня
                level_num = int(achievement_id.split("_")[-1])
                level_info = self.get_level_info(level_num)
                if level_info:
                    new_achievements.append({
                        "id": achievement_id,
                        "info": {
                            "name": f"Новый уровень: {level_info['name']}",
                            "description": f"Достигните уровня {level_info['name']}",
                            "category": "level",
                            "points": 0,
                            "icon": level_info["icon"]
                        }
                    })
            else:
                info = self.get_achievement_info(achievement_id)
                if info:
                    new_achievements.append({
                        "id": achievement_id,
                        "info": info
                    })
        return new_achievements
    
    def clear_new_achievements(self):
        """Очистить список недавно полученных достижений."""
        self.new_achievements = []
    
    # Методы для обновления статистики
    
    def add_educational_hint(self):
        """Добавить образовательную подсказку."""
        self.stats["educational_hints"] += 1
        self.check_achievements()
    
    def add_opening_learned(self, opening_name: str):
        """Добавить изученный дебют."""
        self.stats["openings_learned"].add(opening_name)
        self.check_achievements()
    
    def add_endgame_completed(self):
        """Добавить завершенный эндшпиль."""
        self.stats["endgames_completed"] += 1
        self.check_achievements()
    
    def add_game_played(self):
        """Добавить сыгранную партию."""
        self.stats["games_played"] += 1
        self.check_achievements()
    
    def add_game_won(self):
        """Добавить выигранную партию."""
        self.stats["games_won"] += 1
        self.check_achievements()
    
    def add_checkmate(self):
        """Добавить поставленный мат."""
        self.stats["checkmates"] += 1
        self.check_achievements()
    
    def add_draw(self):
        """Добавить ничью."""
        self.stats["draws"] += 1
        self.check_achievements()
    
    def add_moves(self, count: int = 1):
        """Добавить сделанные ходы."""
        self.stats["moves_made"] += count
        self.check_achievements()
    
    def add_captures(self, count: int = 1):
        """Добавить взятия."""
        self.stats["captures"] += count
        self.check_achievements()
    
    def add_play_time(self, seconds: int):
        """Добавить время игры."""
        self.stats["time_played"] += seconds
        self.check_achievements()
    
    def add_perfect_game(self):
        """Добавить идеальную игру."""
        self.stats["perfect_games"] += 1
        self.check_achievements()
    
    def add_comeback_win(self):
        """Добавить победу после проигрыша."""
        self.stats["comeback_wins"] += 1
        self.check_achievements()
    
    def add_short_game(self):
        """Добавить короткую игру."""
        self.stats["short_games"] += 1
        self.check_achievements()
    
    def add_long_game(self):
        """Добавить длинную игру."""
        self.stats["long_games"] += 1
        self.check_achievements()