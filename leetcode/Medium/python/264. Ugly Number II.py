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
    def nthUglyNumber(self, n):
        """
        Возвращает n-е уродливое число.
        
        Уродливые числа — положительные числа, простые множители которых
        ограничены 2, 3 и 5. Последовательность начинается: 1, 2, 3, 4, 5, 6, 8, 9, 10, 12...
        
        Args:
            n: Порядковый номер уродливого числа (1-индексировано)
            
        Returns:
            n-е уродливое число
            
        Примеры:
            >>> Solution().nthUglyNumber(10)
            12
            >>> Solution().nthUglyNumber(1)
            1
            
        Сложность:
            Время: O(n)
            Память: O(n)
        """
        ugly = [1] * n
        i2 = i3 = i5 = 0
        next2, next3, next5 = 2, 3, 5
        
        for i in range(1, n):
            ugly[i] = min(next2, next3, next5)
            
            if ugly[i] == next2:
                i2 += 1
                next2 = ugly[i2] * 2
            if ugly[i] == next3:
                i3 += 1
                next3 = ugly[i3] * 3
            if ugly[i] == next5:
                i5 += 1
                next5 = ugly[i5] * 5
                
        return ugly[-1]