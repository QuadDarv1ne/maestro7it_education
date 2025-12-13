/*
https://leetcode.com/problems/scramble-string/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

var isScramble = function(s1, s2) {
    if (s1.length !== s2.length) return false;

    let freq = Array(26).fill(0);
    for (let i = 0; i < s1.length; i++) {
        freq[s1.charCodeAt(i)-97]++;
        freq[s2.charCodeAt(i)-97]--;
    }
    if (freq.some(x => x !== 0)) return false;

    const n = s1.length;
    let dp = Array.from({length:n}, () =>
        Array.from({length:n}, () =>
            Array(n+1).fill(false)));

    for (let i = 0; i < n; i++)
        for (let j = 0; j < n; j++)
            dp[i][j][1] = s1[i] === s2[j];

    for (let len = 2; len <= n; len++) {
        for (let i = 0; i + len <= n; i++) {
            for (let j = 0; j + len <= n; j++) {
                for (let k = 1; k < len; k++) {
                    if ((dp[i][j][k] && dp[i+k][j+k][len-k]) ||
                        (dp[i][j+len-k][k] && dp[i+k][j][len-k])) {
                        dp[i][j][len] = true;
                        break;
                    }
                }
            }
        }
    }
    return dp[0][0][n];
};
