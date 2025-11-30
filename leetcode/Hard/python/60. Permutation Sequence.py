'''
https://leetcode.com/problems/permutation-sequence/description/
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Permutation Sequence"

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
'''

class Solution(object):
    def getPermutation(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: str
        """
        # Вычисляем факториалы от 0! до (n-1)!
        factorials = [1] * n
        for i in range(1, n):
            factorials[i] = factorials[i-1] * i
        
        # Создаем список доступных чисел
        numbers = [str(i) for i in range(1, n+1)]
        result = []
        k -= 1  # Переходим к 0-индексации
        
        for i in range(n-1, -1, -1):
            # Определяем индекс текущего числа
            index = k // factorials[i]
            k %= factorials[i]
            
            # Добавляем число в результат и удаляем из доступных
            result.append(numbers[index])
            numbers.pop(index)
        
        return ''.join(result)