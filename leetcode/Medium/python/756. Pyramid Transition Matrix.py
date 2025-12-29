'''
https://leetcode.com/problems/pyramid-transition-matrix/description/
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Pyramid Transition Matrix"

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
'''

from collections import defaultdict
# from typing import List

class Solution:
    def pyramidTransition(self, bottom, allowed):
        """
        Определяет, можно ли построить пирамиду из заданного основания.
        
        Args:
            bottom: строка основания пирамиды
            allowed: список разрешенных троек вида "XYZ", где XY - основание, Z - вершина
            
        Returns:
            True если пирамиду можно построить, иначе False
        """
        # Создаем словарь для быстрого поиска разрешенных вершин
        # Ключ: пара символов (основание), значение: список возможных вершин
        allowed_map = defaultdict(list)
        for triple in allowed:
            base = triple[:2]  # первые два символа
            top = triple[2]    # третий символ
            allowed_map[base].append(top)
        
        # Мемоизация для оптимизации
        memo = {}
        
        def dfs(current_level, next_level, idx):
            """
            Рекурсивно строим следующий уровень пирамиды.
            
            Args:
                current_level: текущий уровень пирамиды
                next_level: строящийся следующий уровень
                idx: текущая позиция в следующем уровне
            """
            # Базовый случай: следующий уровень полностью построен
            if len(next_level) == len(current_level) - 1:
                # Если следующий уровень состоит из одного символа - пирамида построена
                if len(next_level) == 1:
                    return True
                # Иначе рекурсивно строим следующий уровень
                return dfs(next_level, "", 0)
            
            # Текущая пара символов в основании
            pair = current_level[idx:idx+2]
            
            # Если для этой пары нет разрешенных вершин - невозможно построить
            if pair not in allowed_map:
                return False
            
            # Перебираем все возможные вершины для текущей пары
            for top in allowed_map[pair]:
                # Пробуем добавить вершину и продолжить построение
                if dfs(current_level, next_level + top, idx + 1):
                    return True
            
            return False
        
        return dfs(bottom, "", 0)