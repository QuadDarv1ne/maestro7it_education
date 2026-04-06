"""
https://leetcode.com/problems/walking-robot-simulation/description/
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Walking Robot Simulation" на Python

Задача: Робот начинает в (0,0) и выполняет команды: 
        -2 – поворот налево, -1 – поворот направо, 1..9 – шаги вперёд.
        На поле есть препятствия. Нужно найти максимальное квадратичное расстояние
        от начала, которое робот достиг во время движения.

Алгоритм:
1. Задаём направления: север (0,1), восток (1,0), юг (0,-1), запад (-1,0).
2. Препятствия храним в множестве кортежей.
3. Для каждой команды:
   - Если поворот, меняем направление.
   - Если шаги: пытаемся сделать каждый шаг, проверяя следующую клетку.
     Если клетка не препятствие – перемещаемся и обновляем максимальное расстояние.
     Иначе – прерываем шаги для этой команды.
4. Возвращаем максимальное расстояние (x*x + y*y).

Сложность: O(commands + obstacles) времени и памяти.

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
"""

class Solution:
    def robotSim(self, commands, obstacles):
        # Направления: север, восток, юг, запад
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        dir_idx = 0  # начинаем с севера
        
        # Множество препятствий для быстрой проверки
        obs_set = set(map(tuple, obstacles))
        
        x, y = 0, 0
        max_dist = 0
        
        for cmd in commands:
            if cmd == -1:          # поворот направо
                dir_idx = (dir_idx + 1) % 4
            elif cmd == -2:        # поворот налево
                dir_idx = (dir_idx + 3) % 4
            else:
                # Идём вперёд cmd шагов
                dx, dy = dirs[dir_idx]
                for _ in range(cmd):
                    nx, ny = x + dx, y + dy
                    if (nx, ny) not in obs_set:
                        x, y = nx, ny
                        max_dist = max(max_dist, x*x + y*y)
                    else:
                        break
        return max_dist