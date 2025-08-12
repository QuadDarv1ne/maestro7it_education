'''
https://leetcode.com/problems/coin-change/description/?envType=study-plan-v2&envId=top-interview-150
'''

class Solution(object):
    def coinChange(self, coins, amount):
        """
        Найти минимальное количество монет для набора суммы amount.
        Если сумму невозможно составить, вернуть -1.

        :type coins: List[int] - список номиналов монет
        :type amount: int - целевая сумма
        :rtype: int - минимальное количество монет или -1
        """
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0
        
        for coin in coins:
            for x in range(coin, amount + 1):
                if dp[x - coin] != float('inf'):
                    dp[x] = min(dp[x], dp[x - coin] + 1)
        
        return dp[amount] if dp[amount] != float('inf') else -1

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks