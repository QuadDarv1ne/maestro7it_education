"""
3228. Maximum Number of Operations to Move Ones to the End
Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
Источник идеи: LeetCode editorial / walkccc.
"""

class Solution:
    def maxOperations(self, s: str) -> int:
        """
        Итоговый алгоритм:
        - Перебираем строку слева направо, считаем накопленные '1' (ones).
        - Когда встречаем '0', и при этом это либо последний символ, либо следующий символ — '1',
          добавляем в ответ текущее количество ones.
        Это даёт корректное максимальное число операций.
        """
        ans = 0
        ones = 0
        n = len(s)

        for i, ch in enumerate(s):
            if ch == '1':
                ones += 1
            elif i + 1 == n or s[i + 1] == '1':
                ans += ones

        return ans

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks