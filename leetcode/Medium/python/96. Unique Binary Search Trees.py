'''
https://leetcode.com/problems/unique-binary-search-trees/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

class Solution:
    def numTrees(self, n):
        """
        Решение задачи "Unique Binary Search Trees" (LeetCode 96).

        dp[i] — количество уникальных BST из i узлов.

        Сложность:
        - Время: O(n^2)
        - Память: O(n)
        """
        dp = [0] * (n + 1)
        dp[0] = dp[1] = 1

        for nodes in range(2, n + 1):
            for root in range(1, nodes + 1):
                dp[nodes] += dp[root - 1] * dp[nodes - root]

        return dp[n]
