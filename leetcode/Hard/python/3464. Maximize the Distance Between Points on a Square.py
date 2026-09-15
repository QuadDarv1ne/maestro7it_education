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
    def maxDistance(self, side, points, k):
        n = len(points)
        pos = []
        for x, y in points:
            if y == 0:
                pos.append(x)
            elif x == side:
                pos.append(side + y)
            elif y == side:
                pos.append(2 * side + (side - x))
            else:
                pos.append(3 * side + (side - y))
        pos.sort()

        perimeter = 4 * side
        extended = pos + [p + perimeter for p in pos]

        def can_place(d: int) -> bool:
            # Пробуем каждую точку как стартовую
            for start in range(n):
                cnt = 1
                last_pos = extended[start]
                cur_idx = start
                while cnt < k:
                    target = last_pos + d
                    # Бинарный поиск первой позиции >= target
                    next_idx = bisect_left(extended, target, cur_idx + 1, start + n)
                    if next_idx == start + n:
                        break
                    cur_idx = next_idx
                    last_pos = extended[cur_idx]
                    cnt += 1
                # Убеждаемся, что циклическое расстояние до стартовой тоже >= d
                if cnt == k and extended[start] + perimeter - last_pos >= d:
                    return True
            return False

        lo, hi = 0, 2 * side
        ans = 0
        import bisect
        while lo <= hi:
            mid = (lo + hi) // 2
            if can_place(mid):
                ans = mid
                lo = mid + 1
            else:
                hi = mid - 1
        return ans