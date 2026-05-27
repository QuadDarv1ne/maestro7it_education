"""
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
"""

class Solution:
    def numberOfSpecialChars(self, word):
        INF = 10**9
        last_lower = [-1] * 26
        first_upper = [INF] * 26
        
        for i, c in enumerate(word):
            if 'a' <= c <= 'z':
                last_lower[ord(c) - ord('a')] = i
            else:
                idx = ord(c) - ord('A')
                if first_upper[idx] == INF:
                    first_upper[idx] = i
        
        ans = 0
        for i in range(26):
            if last_lower[i] != -1 and first_upper[i] != INF \
               and last_lower[i] < first_upper[i]:
                ans += 1
        return ans