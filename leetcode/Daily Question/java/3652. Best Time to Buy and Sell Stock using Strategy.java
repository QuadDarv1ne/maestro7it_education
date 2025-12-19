/*
https://leetcode.com/problems/best-time-to-buy-and-sell-stock-using-strategy/

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

class Solution {
    public long maxProfit(int[] prices, int[] strategy, int k) {
        int n = prices.length;
        int half = k / 2;

        long base = 0;
        for (int i = 0; i < n; i++)
            base += (long) prices[i] * strategy[i];

        long original = 0, modified = 0;
        for (int i = 0; i < k; i++) {
            original += (long) prices[i] * strategy[i];
            if (i >= half) modified += prices[i];
        }

        long bestDelta = Math.max(0, modified - original);

        for (int r = k; r < n; r++) {
            int l = r - k;

            original -= (long) prices[l] * strategy[l];
            if (l + half < r) modified -= prices[l + half];

            original += (long) prices[r] * strategy[r];
            modified += prices[r];

            bestDelta = Math.max(bestDelta, modified - original);
        }

        return base + bestDelta;
    }
}
