"""
https://leetcode.com/problems/24-game/description/
"""

class Solution:
    def judgePoint24(self, cards):
        """
        Определяет, можно ли из четырех карт составить выражение,
        дающее 24, используя +, -, *, / и скобки.
        """
        EPS = 1e-6

        def helper(nums):
            if len(nums) == 1:
                return abs(nums[0] - 24.0) < EPS
            n = len(nums)
            for i in range(n):
                for j in range(i + 1, n):
                    a, b = nums[i], nums[j]
                    rest = [nums[k] for k in range(n) if k != i and k != j]
                    candidates = [a + b, a - b, b - a, a * b]
                    if abs(b) > EPS: candidates.append(a / b)
                    if abs(a) > EPS: candidates.append(b / a)
                    for c in candidates:
                        if helper(rest + [c]):
                            return True
            return False

        return helper([float(c) for c in cards])

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks