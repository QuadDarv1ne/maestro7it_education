/*
https://leetcode.com/problems/best-time-to-buy-and-sell-stock-using-strategy/

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

public class Solution {
    public long MaxProfit(int[] prices, int[] strategy, int k) {
        int n = prices.Length;
        int half = k / 2;

        long baseProfit = 0;
        for (int i = 0; i < n; i++)
            baseProfit += (long)prices[i] * strategy[i];

        long original = 0, modified = 0;
        for (int i = 0; i < k; i++) {
            original += (long)prices[i] * strategy[i];
            if (i >= half) modified += prices[i];
        }

        long bestDelta = Math.Max(0, modified - original);

        for (int r = k; r < n; r++) {
            int l = r - k;

            original -= (long)prices[l] * strategy[l];
            if (l + half < r) modified -= prices[l + half];

            original += (long)prices[r] * strategy[r];
            modified += prices[r];

            bestDelta = Math.Max(bestDelta, modified - original);
        }

        return baseProfit + bestDelta;
    }
}
