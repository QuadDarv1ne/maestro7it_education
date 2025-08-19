'''
https://leetcode.com/problems/longest-common-prefix/description/
'''

class Solution:
    def longestCommonPrefix(self, strs):
        """
        Возвращает самый длинный общий префикс массива строк.
        Вертикальная проверка: сравниваем символы на каждой позиции.
        """
        if not strs:
            return ""
        for i, ch in enumerate(strs[0]):
            for s in strs[1:]:
                if i >= len(s) or s[i] != ch:
                    return strs[0][:i]
        return strs[0]

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks