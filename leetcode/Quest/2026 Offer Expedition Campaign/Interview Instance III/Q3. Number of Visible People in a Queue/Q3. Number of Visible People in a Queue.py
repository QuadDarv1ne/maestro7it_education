'''
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
'''

class Solution:
    def canSeePersonsCount(self, heights):
        n = len(heights)
        result = [0] * n
        stack = []  # Monotonic decreasing stack (stores indices with decreasing heights from left to right)
        
        for i in range(n - 1, -1, -1):
            visible = 0
            # Pop while current height is greater than stack top's height
            while stack and heights[i] > heights[stack[-1]]:
                stack.pop()
                visible += 1
            # If stack still has elements, the next taller person is visible
            if stack:
                visible += 1
            result[i] = visible
            stack.append(i)
        
        return result