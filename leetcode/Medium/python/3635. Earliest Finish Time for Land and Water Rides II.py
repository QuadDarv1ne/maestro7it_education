"""
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
"""

import bisect

class Solution:
    def earliestFinishTime(self, landStartTime, landDuration, waterStartTime, waterDuration):
        """
        Находит минимальное время завершения одного наземного и одного водного аттракциона.
        
        Турист должен посетить ровно один наземный и ровно один водный аттракцион
        в любом порядке. Аттракцион можно начать в момент его открытия или позже.
        Если аттракцион начат в момент t, он заканчивается в t + duration.
        После завершения одного аттракциона можно сразу начать другой или подождать его открытия.
        
        Алгоритм:
        1. Рассматриваем оба порядка: land→water и water→land
        2. Для каждого аттракциона первого типа находим оптимальный аттракцион второго типа
        3. Используем формулу: finish = max(first_end, second_start) + second_duration
        4. Сортируем аттракционы второго типа по времени начала
        5. Строим префиксные минимумы длительностей и суффиксные минимумы времени завершения
        6. Для каждого первого аттракциона бинарным поиском находим границу
           и за O(1) получаем оптимальное время
        
        Args:
            landStartTime: список времён открытия наземных аттракционов
            landDuration: список длительностей наземных аттракционов
            waterStartTime: список времён открытия водных аттракционов
            waterDuration: список длительностей водных аттракционов
        
        Returns:
            Минимальное возможное время завершения обоих аттракционов
            
        Сложность:
            Время: O(N log M + M log M), где N и M — количество наземных и водных аттракционов
            Память: O(N + M)
        
        Примеры:
            >>> sol = Solution()
            >>> sol.earliestFinishTime([2, 8], [4, 1], [6], [3])
            9
            >>> sol.earliestFinishTime([5], [3], [1], [10])
            14
        """
        
        def solve(first_start, first_dur, second_start, second_dur):
            """
            Вычисляет минимальное время для порядка: сначала first, потом second.
            
            Для каждого аттракциона первого типа перебираем все возможные
            аттракционы второго типа и находим минимальное время завершения.
            Оптимизация достигается за счёт сортировки и предподсчёта минимумов.
            
            Args:
                first_start: времена открытия аттракционов первого типа
                first_dur: длительности аттракционов первого типа
                second_start: времена открытия аттракционов второго типа
                second_dur: длительности аттракционов второго типа
            
            Returns:
                Минимальное время завершения для данного порядка
            """
            n = len(first_start)
            m = len(second_start)
            
            # Создаём список аттракционов второго типа: (start, duration, finish)
            second = []
            for i in range(m):
                start = second_start[i]
                dur = second_dur[i]
                finish = start + dur
                second.append((start, dur, finish))
            
            # Сортируем по времени начала
            second.sort(key=lambda x: x[0])
            
            # Массив времён начала для бинарного поиска
            starts = [s[0] for s in second]
            
            # Префиксный минимум длительностей
            # pref_min_dur[i] = минимальная длительность среди первых i аттракционов
            pref_min_dur = [float('inf')] * (m + 1)
            for i in range(m):
                pref_min_dur[i + 1] = min(pref_min_dur[i], second[i][1])
            
            # Суффиксный минимум времён завершения
            # suff_min_finish[i] = минимальное время завершения среди аттракционов с индексом >= i
            suff_min_finish = [float('inf')] * (m + 1)
            for i in range(m - 1, -1, -1):
                suff_min_finish[i] = min(suff_min_finish[i + 1], second[i][2])
            
            ans = float('inf')
            
            for i in range(n):
                # Время завершения первого аттракциона
                first_end = first_start[i] + first_dur[i]
                
                # Бинарный поиск: находим первый second, у которого start >= first_end
                idx = bisect.bisect_left(starts, first_end)
                
                # Случай 1: second начинается после завершения first (или ровно в момент завершения)
                # finish = second_start + second_duration = second_finish
                # Берём минимальный second_finish среди всех, у которых start >= first_end
                if idx < m:
                    ans = min(ans, suff_min_finish[idx])
                
                # Случай 2: second уже открыт к моменту завершения first
                # finish = first_end + second_duration
                # Берём минимальную second_duration среди всех, у которых start < first_end
                if idx > 0:
                    ans = min(ans, first_end + pref_min_dur[idx])
            
            return ans
        
        # Вычисляем минимальное время для обоих порядков
        land_first = solve(landStartTime, landDuration, waterStartTime, waterDuration)
        water_first = solve(waterStartTime, waterDuration, landStartTime, landDuration)
        
        return min(land_first, water_first)