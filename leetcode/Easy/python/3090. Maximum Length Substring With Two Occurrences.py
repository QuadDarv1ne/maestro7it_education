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

from collections import defaultdict

class Solution:
    def maximumLengthSubstring(self, s):
        """
        Возвращает максимальную длину подстроки, в которой каждый символ
        встречается не более двух раз.
        Используется метод скользящего окна.
        """
        count = defaultdict(int)
        left = 0
        ans = 0

        for right, ch in enumerate(s):
            count[ch] += 1

            while count[ch] > 2:
                count[s[left]] -= 1
                left += 1

            ans = max(ans, right - left + 1)

        return ans