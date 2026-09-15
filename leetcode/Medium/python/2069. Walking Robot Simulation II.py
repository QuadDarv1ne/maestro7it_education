"""
https://leetcode.com/problems/walking-robot-simulation-ii/description/
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Walking Robot Simulation II" на Python

Алгоритм аналогичен C++ версии.

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
"""

class Robot:
    def __init__(self, width, height):
        self.perimeter = 2 * (width + height) - 4
        self.steps = 0
        self.positions = []
        self.directions = []
        
        # Строим периметр против часовой стрелки
        # East
        for x in range(width):
            self.positions.append((x, 0))
            self.directions.append("East")
        # North
        for y in range(1, height):
            self.positions.append((width - 1, y))
            self.directions.append("North")
        # West
        for x in range(width - 2, -1, -1):
            self.positions.append((x, height - 1))
            self.directions.append("West")
        # South
        for y in range(height - 2, 0, -1):
            self.positions.append((0, y))
            self.directions.append("South")
    
    def step(self, num):
        self.steps += num
    
    def getPos(self):
        if self.perimeter == 0:
            return [0, 0]
        idx = self.steps % self.perimeter
        return list(self.positions[idx])
    
    def getDir(self):
        if self.perimeter == 0:
            return "East"
        idx = self.steps % self.perimeter
        # Особый случай: после полного круга смотрим на South
        if self.steps > 0 and idx == 0:
            return "South"
        return self.directions[idx]