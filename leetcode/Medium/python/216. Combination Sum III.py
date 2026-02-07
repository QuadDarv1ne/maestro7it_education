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

class Solution:
    def combinationSum3(self, k, n):
        """
        Находит все комбинации k чисел от 1 до 9, сумма которых равна n.
        
        Args:
            k: Количество чисел в комбинации
            n: Целевая сумма
            
        Returns:
            Список всех уникальных комбинаций
            
        Алгоритм: Backtracking (поиск с возвратом)
        1. Начинаем с пустой комбинации и суммы 0
        2. Рекурсивно добавляем числа от 1 до 9
        3. Если комбинация достигла длины k и суммы n - добавляем в результат
        4. Если сумма превысила n или длина превысила k - прекращаем поиск
        5. Для избежания дубликатов всегда начинаем со следующего числа
        """
        
        result = []
        
        def backtrack(start, current_combination, current_sum):
            """
            Рекурсивная функция для поиска комбинаций
            
            Args:
                start: С какого числа начинать (чтобы избежать дубликатов)
                current_combination: Текущая комбинация
                current_sum: Сумма текущей комбинации
            """
            # Базовый случай: если нашли подходящую комбинацию
            if len(current_combination) == k and current_sum == n:
                # ИСПРАВЛЕНИЕ: используем срез [:] вместо .copy()
                result.append(current_combination[:])
                return
            
            # Если комбинация слишком длинная или сумма слишком большая
            if len(current_combination) > k or current_sum > n:
                return
            
            # Перебираем числа от start до 9
            for num in range(start, 10):
                # Добавляем число в комбинацию
                current_combination.append(num)
                current_sum += num
                
                # Рекурсивный вызов для следующего числа
                backtrack(num + 1, current_combination, current_sum)
                
                # Backtrack: убираем число из комбинации
                current_combination.pop()
                current_sum -= num
        
        # Начинаем поиск с числа 1
        backtrack(1, [], 0)
        
        return result