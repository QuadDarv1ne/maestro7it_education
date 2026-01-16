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
    def minCut(self, s):
        """
        Оптимизированное решение с O(n) памятью.

        Находит минимальное количество разрезов для разбиения строки на палиндромы.

        Алгоритм:
        1. Используем динамическое программирование с проверкой палиндромов на лету
        2. Храним только минимальные разрезы и центры палиндромов
        
        Сложность: O(n²) время, O(n) память
        """
        
        n = len(s)
        if n <= 1:
            return 0
        
        # Массив минимальных разрезов
        # cuts[i] = минимальное количество разрезов для s[0:i+1]
        cuts = [0] * n
        
        # Инициализируем массив максимальными значениями
        for i in range(n):
            cuts[i] = i  # В худшем случае нужно i разрезов
        
        # Центры палиндромов
        for center in range(n):
            # Нечетная длина палиндромов
            left = right = center
            while left >= 0 and right < n and s[left] == s[right]:
                # Если весь текущий палиндром - от 0 до right
                if left == 0:
                    cuts[right] = 0
                else:
                    cuts[right] = min(cuts[right], cuts[left - 1] + 1)
                left -= 1
                right += 1
            
            # Четная длина палиндромов
            left, right = center, center + 1
            while left >= 0 and right < n and s[left] == s[right]:
                if left == 0:
                    cuts[right] = 0
                else:
                    cuts[right] = min(cuts[right], cuts[left - 1] + 1)
                left -= 1
                right += 1
        
        return cuts[n - 1]