'''
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
'''

class Solution:
    def maxPalindromes(self, s, k):
        n = len(s)
        # earliest_end[i] = minimum end index of a palindrome starting at i with length >= k
        earliest_end = [float('inf')] * n
        
        # Helper to expand around center and record palindromes
        def expand(l, r):
            while l >= 0 and r < n and s[l] == s[r]:
                if r - l + 1 >= k:
                    earliest_end[l] = min(earliest_end[l], r)
                l -= 1
                r += 1
        
        # Check both odd and even length palindromes
        for i in range(n):
            expand(i, i)      # odd length
            expand(i, i + 1)  # even length
        
        dp = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            dp[i] = dp[i + 1]  # skip current
            if earliest_end[i] != float('inf'):
                j = earliest_end[i]
                dp[i] = max(dp[i], 1 + dp[j + 1])
        return dp[0]