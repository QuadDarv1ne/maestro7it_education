/*
https://leetcode.com/problems/best-time-to-buy-and-sell-stock-using-strategy/

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

var maxProfit = function(prices, strategy, k) {
    const n = prices.length;
    const half = Math.floor(k / 2);

    let base = 0;
    for (let i = 0; i < n; i++) {
        base += prices[i] * strategy[i];
    }

    let original = 0, modified = 0;
    for (let i = 0; i < k; i++) {
        original += prices[i] * strategy[i];
        if (i >= half) modified += prices[i];
    }

    let bestDelta = Math.max(0, modified - original);

    for (let r = k; r < n; r++) {
        const l = r - k;

        original -= prices[l] * strategy[l];
        if (l + half < r) modified -= prices[l + half];

        original += prices[r] * strategy[r];
        modified += prices[r];

        bestDelta = Math.max(bestDelta, modified - original);
    }

    return base + bestDelta;
};
