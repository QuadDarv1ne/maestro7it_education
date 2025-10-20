# ============================================================================
# utils/endgame_trainer.py
# ============================================================================

"""
Модуль: utils/endgame_trainer.py

Описание:
    Содержит реализацию системы тренировки эндшпилей для шахматной игры chess_stockfish.
    Предоставляет специфические сценарии для изучения эндшпилей различной сложности.
    
Возможности:
    - Тренировка базовых эндшпилей (ферзь против пешки, ладья против пешки)
    - Тренировка пешечных эндшпилей
    - Тренировка эндшпилей с малым количеством фигур
    - Система оценки и обратной связи
"""

from typing import Dict, List, Optional, Tuple
import random

# Базовые эндшпильные сценарии
ENDGAME_SCENARIOS = {
    "ферзь_против_пешки": {
        "name": "Ферзь против пешки",
        "description": "Учимся выигрывать ферзем против пешки",
        "fen": "8/8/8/8/8/8/4k3/K4Q1P w - - 0 1",
        "difficulty": "Начальный",
        "goal": "Превратить пешку в ферзя и выиграть",
        "tips": [
            "Используйте ферзя для ограничения движения короля противника",
            "Не допускайте патта - дайте противнику хотя бы один ход",
            "Контролируйте квадрат превращения пешки"
        ]
    },
    "ладья_против_пешки": {
        "name": "Ладья против пешки",
        "description": "Учимся выигрывать ладьей против пешки",
        "fen": "8/8/8/8/8/8/7k/7K w - - 0 1",
        "difficulty": "Начальный",
        "goal": "Остановить пешку и выиграть",
        "tips": [
            "Используйте ладью для отсечения короля от пешки",
            "Контролируйте горизонталь, на которой находится пешка",
            "Поставьте ладью за пешкой, чтобы атаковать её с тыла"
        ]
    },
    "король_против_пешки": {
        "name": "Король против пешки",
        "description": "Учимся останавливать пешку королем",
        "fen": "8/8/8/8/8/8/7k/7K w - - 0 1",
        "difficulty": "Начальный",
        "goal": "Остановить пешку или превратить свою пешку",
        "tips": [
            "Рассчитайте квадрат превращения пешки",
            "Используйте оппозицию для контроля ключевых полей",
            "Держите своего короля впереди своей пешки"
        ]
    },
    "две_ладьи_против_короля": {
        "name": "Две ладьи против короля",
        "description": "Учимся ставить мат двумя ладьями",
        "fen": "8/8/8/8/8/8/8/RR6k w - - 0 1",
        "difficulty": "Средний",
        "goal": "Поставить мат королю противника",
        "tips": [
            "Используйте одну ладью для ограничения движения короля",
            "Второй ладьей постепенно уменьшайте пространство",
            "Поставьте ладьи на соседние горизонтали или вертикали"
        ]
    },
    "ферзь_против_ладьи": {
        "name": "Ферзь против ладьи",
        "description": "Учимся выигрывать ферзем против ладьи",
        "fen": "8/8/8/8/8/8/8/QR6k w - - 0 1",
        "difficulty": "Средний",
        "goal": "Выиграть ладью",
        "tips": [
            "Используйте ферзя для атаки ладьи с расстояния",
            "Контролируйте важные линии и диагонали",
            "Не позволяйте ладье связывать ваш ферзь"
        ]
    },
    "ладья_против_ладьи": {
        "name": "Ладья против ладьи",
        "description": "Пешечный эндшпиль с ладьями",
        "fen": "8/4k3/8/8/8/8/4K3/7R w - - 0 1",
        "difficulty": "Средний",
        "goal": "Выиграть пешку и превратить свою",
        "tips": [
            "Активная ладья должна быть за пешкой",
            "Пассивная ладья защищает свою пешку",
            "Контролируйте открытые линии"
        ]
    },
    "пешечный_гамбит": {
        "name": "Пешечный гамбит",
        "description": "Учимся играть в пешечных окончаниях",
        "fen": "8/8/8/8/8/8/8/8 w - - 0 1",
        "difficulty": "Сложный",
        "goal": "Создать проходную пешку и превратить её",
        "tips": [
            "Создавайте проходные пешки как можно раньше",
            "Поддерживайте свои пешки королем",
            "Блокируйте пешки противника"
        ]
    },
    "противостояние": {
        "name": "Противостояние",
        "description": "Классическое противостояние пешек",
        "fen": "8/8/8/8/8/8/8/8 w - - 0 1",
        "difficulty": "Сложный",
        "goal": "Выиграть в противостоянии пешек",
        "tips": [
            "Рассчитайте квадрат превращения",
            "Используйте оппозицию",
            "Контролируйте ключевые поля"
        ]
    }
}

# Статистика тренировок
ENDGAME_STATS = {
    "scenarios_completed": 0,
    "total_attempts": 0,
    "successful_attempts": 0,
    "time_spent": 0
}

class EndgameTrainer:
    """
    Класс для тренировки эндшпилей.
    """
    
    def __init__(self):
        self.current_scenario = None
        self.scenario_start_time = 0
        self.attempts = 0
        self.success = False
        self.stats = ENDGAME_STATS.copy()
    
    def get_available_scenarios(self) -> List[Dict]:
        """
        Получить список доступных сценариев.
        
        Возвращает:
            List[Dict]: Список доступных сценариев
        """
        scenarios = []
        for key, scenario in ENDGAME_SCENARIOS.items():
            scenarios.append({
                "id": key,
                "name": scenario["name"],
                "description": scenario["description"],
                "difficulty": scenario["difficulty"]
            })
        return scenarios
    
    def select_scenario(self, scenario_id: str) -> Optional[Dict]:
        """
        Выбрать сценарий для тренировки.
        
        Параметры:
            scenario_id (str): Идентификатор сценария
            
        Возвращает:
            Dict: Информация о сценарии или None если не найден
        """
        if scenario_id in ENDGAME_SCENARIOS:
            self.current_scenario = scenario_id
            self.attempts = 0
            self.success = False
            import time
            self.scenario_start_time = time.time()
            return ENDGAME_SCENARIOS[scenario_id]
        return None
    
    def get_current_scenario(self) -> Optional[Dict]:
        """
        Получить информацию о текущем сценарии.
        
        Возвращает:
            Dict: Информация о текущем сценарии или None
        """
        if self.current_scenario:
            return ENDGAME_SCENARIOS[self.current_scenario]
        return None
    
    def get_scenario_fen(self) -> Optional[str]:
        """
        Получить FEN позицию текущего сценария.
        
        Возвращает:
            str: FEN позиция или None
        """
        if self.current_scenario:
            return ENDGAME_SCENARIOS[self.current_scenario]["fen"]
        return None
    
    def get_random_tip(self) -> Optional[str]:
        """
        Получить случайный совет по текущему сценарию.
        
        Возвращает:
            str: Совет или None
        """
        if self.current_scenario:
            tips = ENDGAME_SCENARIOS[self.current_scenario]["tips"]
            return random.choice(tips)
        return None
    
    def complete_scenario(self, success: bool = True):
        """
        Завершить текущий сценарий.
        
        Параметры:
            success (bool): Успешно ли завершен сценарий
        """
        if self.current_scenario:
            self.stats["total_attempts"] += 1
            if success:
                self.stats["successful_attempts"] += 1
                self.stats["scenarios_completed"] += 1
                self.success = True
            
            import time
            if self.scenario_start_time > 0:
                self.stats["time_spent"] += time.time() - self.scenario_start_time
            
            self.current_scenario = None
            self.scenario_start_time = 0
    
    def get_stats(self) -> Dict:
        """
        Получить статистику тренировок.
        
        Возвращает:
            Dict: Статистика тренировок
        """
        return self.stats.copy()
    
    def get_success_rate(self) -> float:
        """
        Получить процент успешных попыток.
        
        Возвращает:
            float: Процент успешных попыток
        """
        if self.stats["total_attempts"] > 0:
            return (self.stats["successful_attempts"] / self.stats["total_attempts"]) * 100
        return 0.0
    
    def get_recommendation(self) -> Optional[str]:
        """
        Получить рекомендацию по следующему сценарию.
        
        Возвращает:
            str: Рекомендация или None
        """
        # Если нет статистики, рекомендуем начальный сценарий
        if self.stats["total_attempts"] == 0:
            return "ферзь_против_пешки"
        
        # Если успешность низкая, рекомендуем более простой сценарий
        success_rate = self.get_success_rate()
        if success_rate < 50:
            # Ищем начальные сценарии
            for key, scenario in ENDGAME_SCENARIOS.items():
                if scenario["difficulty"] == "Начальный":
                    return key
        
        # Если успешность высокая, рекомендуем более сложный сценарий
        elif success_rate > 80:
            # Ищем сложные сценарии
            for key, scenario in ENDGAME_SCENARIOS.items():
                if scenario["difficulty"] == "Сложный":
                    return key
        
        # Иначе рекомендуем средние сценарии
        for key, scenario in ENDGAME_SCENARIOS.items():
            if scenario["difficulty"] == "Средний":
                return key
        
        return None