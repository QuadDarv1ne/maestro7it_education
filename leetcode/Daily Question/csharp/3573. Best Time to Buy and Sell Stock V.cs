/*
https://leetcode.com/problems/best-time-to-buy-and-sell-stock-v/description/?envType=daily-question&envId=2025-12-17

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Best Time to Buy and Sell Stock V"

DP:
dp[t, s] — максимальная прибыль
t — число завершённых транзакций
s — состояние:
  0 — нет позиции
  1 — long (купили)
  2 — short (продали)

Сложность:
Время: O(n · k)
Память: O(k)
*/

public class Solution {
    public long MaximumProfit(int[] prices, int k) {
        if (k == 0 || prices.Length == 0)
            return 0;

        long NEG_INF = (long)-1e18;
        long[,] dp = new long[k + 1, 3];

        for (int i = 0; i <= k; i++)
            for (int j = 0; j < 3; j++)
                dp[i, j] = NEG_INF;

        dp[0, 0] = 0;

        foreach (int price in prices) {
            long[,] next = (long[,])dp.Clone();

            for (int t = 0; t <= k; t++) {
                if (dp[t, 0] != NEG_INF && t < k) {
                    next[t, 1] = Math.Max(next[t, 1], dp[t, 0] - price);
                    next[t, 2] = Math.Max(next[t, 2], dp[t, 0] + price);
                }
                if (dp[t, 1] != NEG_INF && t < k) {
                    next[t + 1, 0] = Math.Max(next[t + 1, 0], dp[t, 1] + price);
                }
                if (dp[t, 2] != NEG_INF && t < k) {
                    next[t + 1, 0] = Math.Max(next[t + 1, 0], dp[t, 2] - price);
                }
            }
            dp = next;
        }

        long ans = 0;
        for (int t = 0; t <= k; t++)
            ans = Math.Max(ans, dp[t, 0]);

        return ans;
    }
}
