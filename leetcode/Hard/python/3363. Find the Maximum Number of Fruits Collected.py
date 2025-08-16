'''
https://leetcode.com/problems/find-the-maximum-number-of-fruits-collected/description/?envType=daily-question&envId=2025-08-16
'''

class Solution:
    def maxCollectedFruits(self, fruits):
        """
        Делаем DP для двух детей, добавляем фрукты по главной диагонали.
        """
        n = len(fruits)
        inf = float('-inf')

        # DP для ребёнка 2 (сверху-справа)
        f2 = [[inf]*n for _ in range(n)]
        f2[0][n-1] = fruits[0][n-1]
        for i in range(1, n):
            for j in range(i+1, n):
                best_prev = max(f2[i-1][j], f2[i-1][j-1])
                if j+1 < n:
                    best_prev = max(best_prev, f2[i-1][j+1])
                f2[i][j] = best_prev + fruits[i][j]

        # DP для ребёнка 3 (снизу-слева)
        f3 = [[inf]*n for _ in range(n)]
        f3[n-1][0] = fruits[n-1][0]
        for j in range(1, n):
            for i in range(j+1, n):
                best_prev = max(f3[i][j-1], f3[i-1][j-1])
                if i+1 < n:
                    best_prev = max(best_prev, f3[i+1][j-1])
                f3[i][j] = best_prev + fruits[i][j]

        # Считаем сумму по главной диагонали
        diag_sum = sum(fruits[i][i] for i in range(n))
        return diag_sum + f2[n-2][n-1] + f3[n-1][n-2]

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks