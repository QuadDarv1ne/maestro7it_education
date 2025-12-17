'''
https://leetcode.com/problems/best-time-to-buy-and-sell-stock-v/description/?envType=daily-question&envId=2025-12-17
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Best Time to Buy and Sell Stock V"
Максимальная прибыль с не более чем k транзакциями с учетом коротких продаж

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
    def maximumProfit(self, prices, k):
        """
        :type prices: List[int]
        :type k: int
        :rtype: int
        """
        # Если k = 0, то транзакций совершить нельзя
        if k == 0:
            return 0
        
        # Инициализация DP
        INF = 10**18  # Большое отрицательное число для инициализации
        # dp[t][s] - максимальная прибыль после завершения t транзакций и нахождения в состоянии s
        # s = 0: нет открытой транзакции
        # s = 1: открыта нормальная транзакция (купили)
        # s = 2: открыта короткая транзакция (продали)
        dp = [[-INF] * 3 for _ in range(k+1)]
        dp[0][0] = 0  # Начальное состояние: 0 транзакций, ничего не открыто
        
        for price in prices:
            # Создаем копию текущего состояния для обновления
            next_dp = [row[:] for row in dp]
            
            for t in range(k+1):
                # Состояние 0: нет открытой транзакции
                if dp[t][0] != -INF:
                    if t < k:
                        # Открыть нормальную транзакцию (покупка)
                        next_dp[t][1] = max(next_dp[t][1], dp[t][0] - price)
                        # Открыть короткую транзакцию (продажа)
                        next_dp[t][2] = max(next_dp[t][2], dp[t][0] + price)
                
                # Состояние 1: открыта нормальная транзакция (купили)
                if dp[t][1] != -INF:
                    if t < k:
                        # Закрыть нормальную транзакцию (продажа)
                        next_dp[t+1][0] = max(next_dp[t+1][0], dp[t][1] + price)
                
                # Состояние 2: открыта короткая транзакция (продали)
                if dp[t][2] != -INF:
                    if t < k:
                        # Закрыть короткую транзакцию (покупка)
                        next_dp[t+1][0] = max(next_dp[t+1][0], dp[t][2] - price)
            
            # Обновляем состояние для следующего дня
            dp = next_dp
        
        # Находим максимальную прибыль в состоянии 0 (все транзакции завершены)
        ans = 0
        for t in range(k+1):
            ans = max(ans, dp[t][0])
        return ans