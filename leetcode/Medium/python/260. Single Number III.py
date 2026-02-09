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
    def singleNumber(self, nums):
        """
        Находит два числа, которые встречаются в массиве ровно один раз.
        
        Параметры:
        nums (List[int]): Массив целых чисел, в котором каждое число встречается дважды,
                          кроме двух чисел, встречающихся по одному разу.
        
        Возвращает:
        List[int]: Список из двух чисел, которые встречаются по одному разу.
        
        Алгоритм:
        1. Вычисляем XOR всех чисел - получаем XOR двух искомых чисел.
        2. Находим любой отличающийся бит (обычно правый единичный бит).
        3. Разделяем числа на две группы по этому биту и находим XOR в каждой группе.
        
        Пример:
        >>> singleNumber([1,2,1,3,2,5])
        [3, 5]
        
        Сложность:
        Время: O(n), где n - длина массива.
        Память: O(1).
        """
        xor_all = 0
        for num in nums:
            xor_all ^= num
        
        # Находим правый единичный бит
        diff = xor_all & -xor_all
        
        a, b = 0, 0
        for num in nums:
            if num & diff:
                a ^= num
            else:
                b ^= num
        
        return [a, b]