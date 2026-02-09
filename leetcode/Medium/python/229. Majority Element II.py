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

# from typing import List

class Solution:
    def majorityElement(self, nums):
        """
        Находит все элементы, которые встречаются более чем ⌊ n/3 ⌋ раз.
        
        Алгоритм (алгоритм Бойера-Мура для k = n/3):
        1. Не может быть более 2 элементов, удовлетворяющих условию.
        2. Используем двух кандидатов и их счетчики.
        3. Первый проход: находим двух кандидатов.
        4. Второй проход: проверяем, действительно ли кандидаты встречаются > n/3 раз.
        
        Сложность:
        Время: O(n), два прохода по массиву
        Пространство: O(1), используем только фиксированное количество переменных
        
        Параметры:
        ----------
        nums : List[int]
            Входной массив целых чисел
            
        Возвращает:
        -----------
        List[int]
            Список элементов, встречающихся более чем ⌊ n/3 ⌋ раз
            
        Примеры:
        --------
        majorityElement([3,2,3]) → [3]
        majorityElement([1]) → [1]
        majorityElement([1,2]) → [1,2]
        majorityElement([1,1,1,3,3,2,2,2]) → [1,2]
        """
        if not nums:
            return []
        
        # Инициализация кандидатов и счетчиков
        candidate1, candidate2 = None, None
        count1, count2 = 0, 0
        
        # Первый проход: поиск кандидатов
        for num in nums:
            if candidate1 is not None and num == candidate1:
                count1 += 1
            elif candidate2 is not None and num == candidate2:
                count2 += 1
            elif count1 == 0:
                candidate1 = num
                count1 = 1
            elif count2 == 0:
                candidate2 = num
                count2 = 1
            else:
                count1 -= 1
                count2 -= 1
        
        # Второй проход: проверка кандидатов
        result = []
        count1, count2 = 0, 0
        n = len(nums)
        
        for num in nums:
            if candidate1 is not None and num == candidate1:
                count1 += 1
            elif candidate2 is not None and num == candidate2:
                count2 += 1
        
        if count1 > n // 3:
            result.append(candidate1)
        if count2 > n // 3:
            result.append(candidate2)
        
        return result
    
    def majorityElement_hashmap(self, nums):
        """
        Решение с использованием хэш-таблицы (не соответствует ограничению O(1) памяти).
        
        Параметры:
        ----------
        nums : List[int]
            Входной массив
            
        Возвращает:
        -----------
        List[int]
            Список элементов, встречающихся более чем ⌊ n/3 ⌋ раз
        """
        from collections import Counter
        
        if not nums:
            return []
        
        counter = Counter(nums)
        n = len(nums)
        result = []
        
        for num, count in counter.items():
            if count > n // 3:
                result.append(num)
        
        return result