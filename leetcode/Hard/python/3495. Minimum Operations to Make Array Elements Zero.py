'''
https://leetcode.com/problems/minimum-operations-to-make-array-elements-zero/description/?envType=daily-question&envId=2025-09-06
'''

class Solution:
    """
    Задача: Для каждого запроса [l, r] вычислить минимальное количество операций,
    чтобы сделать все числа равными нулю.
    Операция: взять два числа и заменить их на floor(a/4) и floor(b/4).
    Ответ: сумма минимальных операций для всех запросов.
    """
    def minOperations(self, queries):
        def get_ops(n):
            res = 0
            ops = 0
            pw = 1
            while pw <= n:
                ops += 1
                l = pw
                r = min(n, pw * 4 - 1)
                res += (r - l + 1) * ops
                pw *= 4
            return res

        total = 0
        for l, r in queries:
            total += (get_ops(r) - get_ops(l - 1) + 1) // 2
        return total

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks