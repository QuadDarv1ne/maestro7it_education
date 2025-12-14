/*
https://leetcode.com/problems/unique-binary-search-trees/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

var numTrees = function(n) {
    const dp = new Array(n + 1).fill(0);
    dp[0] = dp[1] = 1;

    for (let nodes = 2; nodes <= n; nodes++) {
        for (let root = 1; root <= nodes; root++) {
            dp[nodes] += dp[root - 1] * dp[nodes - root];
        }
    }
    return dp[n];
};
