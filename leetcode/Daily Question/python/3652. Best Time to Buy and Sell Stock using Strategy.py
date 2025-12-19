"""
https://leetcode.com/problems/best-time-to-buy-and-sell-stock-using-strategy/

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи:
"Best Time to Buy and Sell Stock Using Strategy"

Ключевая идея:
- Считаем базовую прибыль
- Для каждого окна длины k считаем:
  * исходный вклад
  * вклад после применения стратегии
- Стратегию можно НЕ применять, если она ухудшает результат
- Итоговая прибыль = base + max(0, best_delta)

Сложность:
- Время: O(n)
- Память: O(1)
"""

class Solution(object):
    def maxProfit(self, prices, strategy, k):
        """
        :type prices: List[int]
        :type strategy: List[int]
        :type k: int
        :rtype: int
        """
        n = len(prices)
        half = k // 2

        # 1. Базовая прибыль
        base_profit = 0
        for i in range(n):
            base_profit += prices[i] * strategy[i]

        # 2. Начальное окно
        original = 0  # вклад стратегии на окне
        modified = 0  # вклад после применения новой стратегии

        for i in range(k):
            original += prices[i] * strategy[i]
            if i >= half:
                modified += prices[i]  # вторая половина -> 1

        best_delta = max(0, modified - original)

        # 3. Скользящее окно
        for r in range(k, n):
            l = r - k

            # удаляем левый элемент
            original -= prices[l] * strategy[l]
            if l + half < r:
                modified -= prices[l + half]

            # добавляем правый элемент
            original += prices[r] * strategy[r]
            modified += prices[r]

            best_delta = max(best_delta, modified - original)

        return base_profit + best_delta
