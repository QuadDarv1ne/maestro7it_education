'''
https://leetcode.com/problems/number-of-smooth-descent-periods-of-a-stock/description/?envType=daily-question&envId=2025-12-15

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Number of Smooth Descent Periods of a Stock"

Идея:
dp — длина текущего гладкого убывания.
Если prices[i-1] - prices[i] == 1, то dp увеличивается,
иначе сбрасывается в 1.
Суммируем dp на каждом шаге.

Сложность:
Время: O(n)
Память: O(1)
'''

class Solution(object):
    def getDescentPeriods(self, prices):
        """
        :type prices: List[int]
        :rtype: int
        """
        ans = 0
        dp = 1  # длина текущего smooth descent

        ans += dp
        for i in range(1, len(prices)):
            if prices[i - 1] - prices[i] == 1:
                dp += 1
            else:
                dp = 1
            ans += dp

        return ans
