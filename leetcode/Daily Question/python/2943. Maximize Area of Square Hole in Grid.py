"""
Максимальная площадь квадратного отверстия в сетке

Сложность: O(h log h + v log v) время, O(1) память

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
    def maximizeSquareHoleArea(self, n, m, hBars, vBars):
        hBars.sort()
        vBars.sort()
        
        def max_consecutive(arr):
            if not arr:
                return 0
            max_gap = 1
            current = 1
            for i in range(1, len(arr)):
                if arr[i] == arr[i-1] + 1:
                    current += 1
                else:
                    max_gap = max(max_gap, current)
                    current = 1
            return max(max_gap, current)
        
        max_h = max_consecutive(hBars)
        max_v = max_consecutive(vBars)
        
        side = min(max_h, max_v) + 1
        return side * side