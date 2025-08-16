'''
https://leetcode.com/problems/group-anagrams/description/
'''

from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs):
        """
        Группируем анаграммы:
        - Считаем буквы (size 26) для каждой строки.
        - Используем кортеж счётчиков как ключ в словаре.
        """
        d = defaultdict(list)
        for s in strs:
            count = [0] * 26
            for c in s:
                count[ord(c) - ord('a')] += 1
            d[tuple(count)].append(s)
        return list(d.values())

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks