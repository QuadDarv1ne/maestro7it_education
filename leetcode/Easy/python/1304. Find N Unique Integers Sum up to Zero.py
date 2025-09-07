'''
https://leetcode.com/problems/find-n-unique-integers-sum-up-to-zero/description/?envType=daily-question&envId=2025-09-07
'''

class Solution:
    """
    Возвращает список из n уникальных целых, сумма которых равна 0.
    Алгоритм: если n нечётное — добавляем 0, затем пары (i, -i).
    """
    def sumZero(self, n):
        answer = []
        if n % 2 == 1:
            answer.append(0)
        half = n // 2
        for i in range(1, half + 1):
            answer.append(i)
            answer.append(-i)
        return answer

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks