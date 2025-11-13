'''
https://leetcode.com/problems/ones-and-zeroes/  

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X  
GitHub: https://github.com/QuadDarv1ne/  
'''

class Solution(object):
    def findMaxForm(self, strs, m, n):
        """
        Решает задачу "Ones and Zeroes" (LeetCode 474).

        Задача:
        Дан массив бинарных строк strs и два целых числа m и n.
        Найти наибольшее количество строк из strs, которые можно сформировать,
        используя не более m нулей и n единиц.

        Решение:
        - Динамическое программирование (2D knapsack).
        - dp[i][j] — максимальное количество строк, которые можно собрать,
          используя не более i нулей и j единиц.
        - Для каждой строки подсчитываем кол-во '0' и '1', затем обновляем dp
          в обратном порядке, чтобы избежать переиспользования текущей строки.
        """
        # dp[i][j] — макс. кол-во строк при i нулях и j единицах
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for s in strs:
            zeros = s.count('0')
            ones = s.count('1')
            # Обновляем dp с конца, чтобы не использовать одну строку дважды
            for i in range(m, zeros - 1, -1):
                for j in range(n, ones - 1, -1):
                    dp[i][j] = max(dp[i][j], dp[i - zeros][j - ones] + 1)

        return dp[m][n]

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07   
# 2. Telegram №1 @quadd4rv1n7 
# 3. Telegram №2 @dupley_maxim_1999 
# 4. Rutube канал: https://rutube.ru/channel/4218729/  
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ  
# 6. YouTube канал: https://www.youtube.com/@it-coders  
# 7. ВК группа: https://vk.com/science_geeks