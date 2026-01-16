class Solution:
    def longestConsecutive(self, nums):
        """
        Находит длину самой длинной последовательности последовательных чисел.
        
        Алгоритм:
        1. Преобразуем массив в множество для быстрого поиска
        2. Для каждого числа проверяем, является ли оно началом последовательности
        3. Если да, то подсчитываем длину последовательности
        
        Сложность: O(n) время, O(n) память
        
        Пример:
        Вход: [100, 4, 200, 1, 3, 2]
        Выход: 4 (последовательность 1, 2, 3, 4)

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
        
        if not nums:
            return 0
        
        # Преобразуем в множество для O(1) поиска
        num_set = set(nums)
        max_length = 0
        
        for num in num_set:
            # Проверяем, является ли число началом последовательности
            if num - 1 not in num_set:
                current_num = num
                current_length = 1
                
                # Подсчитываем длину последовательности
                while current_num + 1 in num_set:
                    current_num += 1
                    current_length += 1
                
                # Обновляем максимальную длину
                max_length = max(max_length, current_length)
        
        return max_length