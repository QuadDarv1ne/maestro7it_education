import heapq
# from typing import List

class Solution:
    def mostBooked(self, n, meetings):
        """
        Находит номер комнаты, в которой прошло больше всего встреч.
        
        Args:
            n: количество комнат (0..n-1)
            meetings: список встреч [начало, конец]
            
        Returns:
            Номер комнаты с максимальным количеством встреч (наименьший при равенстве)
            
        Автор: Дуплей Максим Игоревич
        ORCID: https://orcid.org/0009-0007-7605-539X
        GitHub: https://github.com/QuadDarv1ne/
        """
        # Сортируем встречи по времени начала
        meetings.sort()
        
        # Инициализируем доступные комнаты (все свободны в начале)
        # Храним только номера комнат, так как они уже отсортированы
        free_rooms = list(range(n))
        heapq.heapify(free_rooms)
        
        # Куча занятых комнат: (время окончания встречи, номер комнаты)
        # Используем Python int (поддерживает большие числа)
        busy_rooms = []
        
        # Счетчик встреч для каждой комнаты
        room_count = [0] * n
        
        # Текущее время (для обработки отложенных встреч)
        current_time = 0
        
        for start, end in meetings:
            # 1. Освобождаем все комнаты, чьи встречи закончились к времени start
            while busy_rooms and busy_rooms[0][0] <= start:
                end_time, room = heapq.heappop(busy_rooms)
                heapq.heappush(free_rooms, room)
            
            # Обновляем current_time
            current_time = max(current_time, start)
            
            # 2. Если есть свободные комнаты, используем комнату с наименьшим номером
            if free_rooms:
                room = heapq.heappop(free_rooms)
                room_count[room] += 1
                # Встреча начинается в текущее время
                heapq.heappush(busy_rooms, (current_time + (end - start), room))
            
            # 3. Если нет свободных комнат, ждем освобождения первой
            else:
                # Берем комнату, которая освободится раньше всех
                end_time, room = heapq.heappop(busy_rooms)
                
                # Встреча задерживается до освобождения комнаты
                current_time = max(current_time, end_time)
                room_count[room] += 1
                
                # Новая встреча начинается сразу после окончания предыдущей
                # Сохраняем оригинальную длительность встречи
                heapq.heappush(busy_rooms, (current_time + (end - start), room))
        
        # Находим комнату с максимальным количеством встреч
        max_count = max(room_count)
        for i in range(n):
            if room_count[i] == max_count:
                return i
        
        return 0  # На всякий случай
    
''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks