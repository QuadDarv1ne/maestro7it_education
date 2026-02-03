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

class Solution(object):
    def isTrionic(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        
        Проверяет, является ли массив трионическим.
        
        Алгоритм:
        1. Перебираем все возможные позиции p (1..n-3) и q (p+1..n-2)
        2. Для каждой пары (p, q) проверяем:
           - Сегмент [0, p] строго возрастает
           - Сегмент [p, q] строго убывает
           - Сегмент [q, n-1] строго возрастает
        3. Если найдется хоть одна подходящая пара, возвращаем True
        
        Примеры:
        >>> Solution().isTrionic([1, 3, 5, 4, 2, 6])
        True
        >>> Solution().isTrionic([2, 1, 3])
        False
        
        Примечания:
        - p и q не могут быть граничными индексами
        - Все сегменты должны содержать минимум 2 элемента
        - Проверяем строгую монотонность (без равенств)
        """
        n = len(nums)
        
        # Массив должен иметь минимум 3 элемента для возможного разбиения
        if n < 3:
            return False
        
        # Вспомогательные функции для проверки монотонности
        def is_increasing(start, end):
            """Проверяет строгое возрастание сегмента от start до end включительно"""
            for i in range(start, end):
                if nums[i] >= nums[i + 1]:  # Нарушение строгого возрастания
                    return False
            return True
        
        def is_decreasing(start, end):
            """Проверяет строгое убывание сегмента от start до end включительно"""
            for i in range(start, end):
                if nums[i] <= nums[i + 1]:  # Нарушение строгого убывания
                    return False
            return True
        
        # Перебираем все возможные p и q
        # p: от 1 до n-3 (должен оставить место для q и последнего элемента)
        # q: от p+1 до n-2 (должен оставить место для последнего элемента)
        for p in range(1, n - 2):
            for q in range(p + 1, n - 1):
                # Проверяем три условия трионического массива
                if (is_increasing(0, p) and      # Первая часть: строго возрастает
                    is_decreasing(p, q) and      # Средняя часть: строго убывает
                    is_increasing(q, n - 1)):    # Последняя часть: строго возрастает
                    return True  # Нашли подходящее разбиение
        
        # Ни одна пара p, q не подошла
        return False