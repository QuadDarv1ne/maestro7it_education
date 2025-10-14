'''
https://leetcode.com/problems/taking-maximum-energy-from-the-mystic-dungeon/description/?envType=daily-question&envId=2025-10-10
'''

from typing import List

class Solution:
    def maximumEnergy(self, energy: List[int], k: int) -> int:
        """
        Вычисляет максимальную энергию, которую можно получить,
        начиная с некоторого мага и прыгая через k шагов каждый раз.
        DP с обратным накоплением: dp[i] = energy[i] + (dp[i + k] если существует).
        """
        n = len(energy)
        dp = energy[:]  # копия — будем хранить здесь суммы
        # идём с конца к началу
        for i in range(n - 1, -1, -1):
            j = i + k
            if j < n:
                dp[i] += dp[j]
        return max(dp)

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks