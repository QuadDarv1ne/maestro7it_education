'''
https://leetcode.com/problems/interleaving-string/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

class Solution:
    def isInterleave(self, s1, s2, s3):
        """
        Решение задачи "Interleaving String" (LeetCode 97).

        dp[i][j] = True, если s3[:i+j] можно получить
        из s1[:i] и s2[:j].

        Сложность:
        - Время: O(n * m)
        - Память: O(n * m)
        """
        n, m = len(s1), len(s2)
        if n + m != len(s3):
            return False

        dp = [[False] * (m + 1) for _ in range(n + 1)]
        dp[0][0] = True

        for i in range(n + 1):
            for j in range(m + 1):
                if i > 0 and s1[i - 1] == s3[i + j - 1]:
                    dp[i][j] |= dp[i - 1][j]
                if j > 0 and s2[j - 1] == s3[i + j - 1]:
                    dp[i][j] |= dp[i][j - 1]

        return dp[n][m]
