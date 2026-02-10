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

# The isBadVersion API is already defined for you.
# def isBadVersion(version: int) -> bool:

class Solution:
    def firstBadVersion(self, n):
        """
        Находит первую плохую версию с помощью бинарного поиска.
        
        Args:
            n: Количество версий (от 1 до n)
            
        Returns:
            Первая версия, которая является плохой
            
        Пример:
            Если isBadVersion(4) == True, а isBadVersion(3) == False,
            то первая плохая версия = 4
            
        Сложность:
            Время: O(log n)
            Память: O(1)
        """
        left, right = 1, n
        
        while left < right:
            # Избегаем переполнения
            mid = left + (right - left) // 2
            
            if isBadVersion(mid):
                # mid может быть первой плохой версией
                right = mid
            else:
                # Плохая версия находится справа
                left = mid + 1
                
        return left  # или right, так как left == right