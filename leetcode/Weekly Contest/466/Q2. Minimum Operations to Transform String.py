'''
https://leetcode.com/contest/weekly-contest-466/problems/minimum-operations-to-transform-string/description/
'''

class Solution:
    def minOperations(self, s: str) -> int:
        m=26
        for c in s:
            if c!='a':
                v=ord(c)-97
                if v<m: m=v
        return 0 if m==26 else 26-m

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks