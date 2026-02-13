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
    def longestBalanced(self, s):
        n = len(s)
        ans = 0

        # ---------- Случай 1: один символ ----------
        for ch in 'abc':
            cur = 0
            for c in s:
                if c == ch:
                    cur += 1
                    ans = max(ans, cur)
                else:
                    cur = 0

        # ---------- Случай 2: ровно два символа ----------
        pairs = [('a','b'), ('a','c'), ('b','c')]
        for x, y in pairs:
            third = chr(ord('a') + ord('b') + ord('c') - ord(x) - ord(y))
            segments = s.split(third)
            for seg in segments:
                m = len(seg)
                if m < 2:
                    continue
                pref_x = [0] * (m + 1)
                pref_y = [0] * (m + 1)
                for i, ch in enumerate(seg):
                    pref_x[i+1] = pref_x[i] + (1 if ch == x else 0)
                    pref_y[i+1] = pref_y[i] + (1 if ch == y else 0)
                first_occ = {0: 0}
                diff = 0
                for i in range(1, m+1):
                    if seg[i-1] == x:
                        diff += 1
                    elif seg[i-1] == y:
                        diff -= 1
                    if diff in first_occ:
                        start = first_occ[diff]
                        if pref_x[i] - pref_x[start] > 0 and pref_y[i] - pref_y[start] > 0:
                            ans = max(ans, i - start)
                    else:
                        first_occ[diff] = i

        # ---------- Случай 3: три символа ----------
        occ = {(0, 0): (-1, 0, 0, 0)}
        cnt_a = cnt_b = cnt_c = 0
        for i, ch in enumerate(s):
            if ch == 'a':
                cnt_a += 1
            elif ch == 'b':
                cnt_b += 1
            else:
                cnt_c += 1
            key = (cnt_b - cnt_a, cnt_c - cnt_a)
            if key in occ:
                idx, ca, cb, cc = occ[key]
                if cnt_a - ca > 0 and cnt_b - cb > 0 and cnt_c - cc > 0:
                    ans = max(ans, i - idx)
            else:
                occ[key] = (i, cnt_a, cnt_b, cnt_c)

        return ans