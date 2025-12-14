/*
https://leetcode.com/problems/interleaving-string/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

var isInterleave = function(s1, s2, s3) {
    const n = s1.length, m = s2.length;
    if (n + m !== s3.length) return false;

    const dp = Array.from({ length: n + 1 }, () => Array(m + 1).fill(false));
    dp[0][0] = true;

    for (let i = 0; i <= n; i++) {
        for (let j = 0; j <= m; j++) {
            if (i > 0 && s1[i - 1] === s3[i + j - 1])
                dp[i][j] ||= dp[i - 1][j];
            if (j > 0 && s2[j - 1] === s3[i + j - 1])
                dp[i][j] ||= dp[i][j - 1];
        }
    }
    return dp[n][m];
};
