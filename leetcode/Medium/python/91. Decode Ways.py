'''
https://leetcode.com/problems/decode-ways/description/
'''

# from typing import NamedTuple

class Solution:
    def numDecodings(self, s):
        """
        Подсчитывает количество способов декодирования строки digits → буквы (1-26 → A-Z).

        :param s: строка цифр
        :return: число способов декодирования

        Алгоритм:
        dp[0] = 1
        dp[1] = 1 (если s[0] ≠ '0')
        Для i в 2..n:
          если s[i-1] ≠ '0': dp[i] += dp[i-1]
          если 10 ≤ int(s[i-2:i]) ≤ 26: dp[i] += dp[i-2]

        Время: O(n)
        Память: O(n)
        """
        if not s or s[0] == '0':
            return 0
        n = len(s)
        dp = [0] * (n + 1)
        dp[0] = 1
        dp[1] = 1
        for i in range(2, n + 1):
            if s[i - 1] != '0':
                dp[i] += dp[i - 1]
            two = s[i - 2:i]
            if s[i - 2] != '0' and 10 <= int(two) <= 26:
                dp[i] += dp[i - 2]
        return dp[n]

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks