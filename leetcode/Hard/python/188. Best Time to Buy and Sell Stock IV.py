"""
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
"""

class Solution(object):
    def maxProfit(self, k, prices):
        """
        Найти максимальную прибыль от транзакций с акциями при ограничении на количество транзакций.
        
        Параметры:
        k (int): Максимальное количество разрешенных транзакций (покупка + продажа = 1 транзакция)
        prices (List[int]): Список цен акций по дням
        
        Возвращает:
        int: Максимальная прибыль
        
        Алгоритм:
        1. Если k >= n/2, где n = len(prices), то задача сводится к неограниченному числу транзакций.
           В этом случае можно получить прибыль от каждой растущей пары дней.
        2. Иначе используется динамическое программирование с массивами buy и sell.
        
        Сложность:
        Время: O(n*k) при k < n/2, иначе O(n)
        Память: O(k)
        
        Пример:
        >>> solution = Solution()
        >>> solution.maxProfit(2, [3,2,6,5,0,3])
        7
        """
        n = len(prices)
        if n <= 1 or k == 0:
            return 0
        
        # Если k достаточно большое, можно использовать алгоритм для неограниченного числа транзакций
        if k >= n // 2:
            profit = 0
            for i in range(1, n):
                if prices[i] > prices[i-1]:
                    profit += prices[i] - prices[i-1]
            return profit
        
        # Динамическое программирование
        # buy[i] - максимальная прибыль после i покупок, держа акцию
        # sell[i] - максимальная прибыль после i продаж, не держа акцию
        buy = [-float('inf')] * (k + 1)
        sell = [0] * (k + 1)
        
        for price in prices:
            for i in range(k, 0, -1):
                # Чтобы купить на i-й транзакции, нужно было продать на (i-1)-й транзакции
                buy[i] = max(buy[i], sell[i-1] - price)
                # Чтобы продать на i-й транзакции, нужно было купить на i-й транзакции
                sell[i] = max(sell[i], buy[i] + price)
        
        return sell[k]