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
    def score(self, cards, x):
        xid = ord(x) - ord('a')
        cntA = [0] * 10
        cntB = [0] * 10
        cntC = 0

        for card in cards:
            a = ord(card[0]) - ord('a')
            b = ord(card[1]) - ord('a')
            if a == xid and b == xid:
                cntC += 1
            elif a == xid:
                cntA[b] += 1
            elif b == xid:
                cntB[a] += 1

        def compute_g(cnt):
            # выбираем только ненулевые количества и сортируем по убыванию
            vals = [c for c in cnt if c > 0]
            vals.sort(reverse=True)
            vals.append(0)                # фиктивный ноль для удобства
            m = len(vals)

            # t[i] – сколько карт надо удалить, чтобы максимальная группа стала не больше vals[i]
            t = [0] * m
            for i in range(1, m):
                t[i] = t[i-1] + (vals[i-1] - vals[i]) * i

            total = sum(cnt)               # общее количество карт в этой группе
            g = [0] * (total + 1)

            for k in range(total + 1):
                # находим интервал, в котором лежит k
                i = 0
                while i < m - 1 and k >= t[i+1]:
                    i += 1
                group_cnt = i + 1           # сколько групп имеют максимальное значение
                # максимальное оставшееся после удаления k карт
                max_rem = vals[i] - (k - t[i]) // group_cnt
                rem = total - k
                pairs = min(rem // 2, rem - max_rem)
                g[k] = k + pairs
            return g

        gA = compute_g(cntA)
        gB = compute_g(cntB)
        totalA = len(gA) - 1
        totalB = len(gB) - 1

        ans = 0
        for cA in range(min(cntC, totalA) + 1):
            cB = min(cntC - cA, totalB)
            ans = max(ans, gA[cA] + gB[cB])
        return ans
