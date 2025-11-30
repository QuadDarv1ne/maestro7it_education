'''
https://leetcode.com/problems/wildcard-matching/description/
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Wildcard Matching"

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
    def isMatch(self, s, p):
        """
        :type s: str
        :type p: str
        :rtype: bool
        """
        m, n = len(s), len(p)
        # Создаем DP таблицу
        dp = [[False] * (n + 1) for _ in range(m + 1)]
        
        # Базовый случай: пустая строка и пустой паттерн
        dp[0][0] = True
        
        # Обрабатываем случай, когда паттерн начинается с '*'
        for j in range(1, n + 1):
            if p[j-1] == '*':
                dp[0][j] = dp[0][j-1]
        
        # Заполняем DP таблицу
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if p[j-1] == '*':
                    # '*' может соответствовать:
                    # 1. Пустой последовательности: dp[i][j-1]
                    # 2. Одному или более символам: dp[i-1][j]
                    dp[i][j] = dp[i][j-1] or dp[i-1][j]
                elif p[j-1] == '?' or p[j-1] == s[i-1]:
                    # '?' соответствует любому одному символу
                    # Или символы совпадают
                    dp[i][j] = dp[i-1][j-1]
        
        return dp[m][n]