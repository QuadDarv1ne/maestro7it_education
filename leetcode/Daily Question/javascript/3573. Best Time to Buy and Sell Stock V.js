/*
https://leetcode.com/problems/best-time-to-buy-and-sell-stock-v/description/?envType=daily-question&envId=2025-12-17

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Описание:
DP с тремя состояниями.
JS Number безопасен для значений до 1e15+, поэтому BigInt не требуется.
*/

var maximumProfit = function(prices, k) {
    if (k === 0 || prices.length === 0) return 0;

    const NEG_INF = -1e18;
    let dp = Array.from({ length: k + 1 }, () => Array(3).fill(NEG_INF));
    dp[0][0] = 0;

    for (let price of prices) {
        let next = dp.map(row => row.slice());

        for (let t = 0; t <= k; t++) {
            if (dp[t][0] !== NEG_INF && t < k) {
                next[t][1] = Math.max(next[t][1], dp[t][0] - price);
                next[t][2] = Math.max(next[t][2], dp[t][0] + price);
            }
            if (dp[t][1] !== NEG_INF && t < k) {
                next[t + 1][0] = Math.max(next[t + 1][0], dp[t][1] + price);
            }
            if (dp[t][2] !== NEG_INF && t < k) {
                next[t + 1][0] = Math.max(next[t + 1][0], dp[t][2] - price);
            }
        }
        dp = next;
    }

    return Math.max(...dp.map(row => row[0]));
};
