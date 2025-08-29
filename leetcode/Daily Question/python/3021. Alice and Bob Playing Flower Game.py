'''
https://leetcode.com/problems/alice-and-bob-playing-flower-game/description/?envType=daily-question&envId=2025-08-29
'''

# Python
class Solution:
    def flowerGame(self, n, m):
        """
        Вычислить число пар (x, y), 1 ≤ x ≤ n, 1 ≤ y ≤ m, при которых Alice гарантированно выиграет.
        Alice побеждает тогда и только тогда, когда x + y — нечётно.
        """
        x_even = n // 2
        x_odd = (n + 1) // 2
        y_even = m // 2
        y_odd = (m + 1) // 2
        return x_even * y_odd + x_odd * y_even

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks