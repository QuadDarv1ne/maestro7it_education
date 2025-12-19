/*
https://leetcode.com/problems/best-time-to-buy-and-sell-stock-using-strategy/

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Идея:
- Считаем базовую прибыль
- Для каждого окна длины k считаем дельту
- Берём максимальную неотрицательную дельту
*/

class Solution {
public:
    long long maxProfit(vector<int>& prices, vector<int>& strategy, int k) {
        int n = prices.size();
        int half = k / 2;

        long long base = 0;
        for (int i = 0; i < n; i++)
            base += 1LL * prices[i] * strategy[i];

        long long original = 0, modified = 0;
        for (int i = 0; i < k; i++) {
            original += 1LL * prices[i] * strategy[i];
            if (i >= half) modified += prices[i];
        }

        long long bestDelta = max(0LL, modified - original);

        for (int r = k; r < n; r++) {
            int l = r - k;

            original -= 1LL * prices[l] * strategy[l];
            if (l + half < r) modified -= prices[l + half];

            original += 1LL * prices[r] * strategy[r];
            modified += prices[r];

            bestDelta = max(bestDelta, modified - original);
        }

        return base + bestDelta;
    }
};
