/**
 * https://leetcode.com/problems/best-time-to-buy-and-sell-stock-v/description/?envType=daily-question&envId=2025-12-17
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "Best Time to Buy and Sell Stock V"
 * Максимальная прибыль с не более чем k транзакциями с учетом коротких продаж
 */

#include <vector>
#include <algorithm>
#include <climits>

using namespace std;

class Solution {
public:
    long long maximumProfit(vector<int>& prices, int k) {
        if (k == 0 || prices.empty()) return 0;

        const long long NEG_INF = -1e18;
        vector<vector<long long>> dp(k + 1, vector<long long>(3, NEG_INF));
        dp[0][0] = 0;

        for (int price : prices) {
            auto next = dp;
            for (int t = 0; t <= k; ++t) {
                if (dp[t][0] != NEG_INF && t < k) {
                    next[t][1] = max(next[t][1], dp[t][0] - price);
                    next[t][2] = max(next[t][2], dp[t][0] + price);
                }
                if (dp[t][1] != NEG_INF && t < k) {
                    next[t + 1][0] = max(next[t + 1][0], dp[t][1] + price);
                }
                if (dp[t][2] != NEG_INF && t < k) {
                    next[t + 1][0] = max(next[t + 1][0], dp[t][2] - price);
                }
            }
            dp.swap(next);
        }

        long long ans = 0;
        for (int t = 0; t <= k; ++t)
            ans = max(ans, dp[t][0]);

        return ans;
    }
};
