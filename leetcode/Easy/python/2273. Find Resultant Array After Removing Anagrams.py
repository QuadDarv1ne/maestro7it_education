'''
https://leetcode.com/problems/find-resultant-array-after-removing-anagrams/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

class Solution:
    def removeAnagrams(self, words):
        result = []
        prev = ""
        for word in words:
            sorted_word = ''.join(sorted(word))
            if sorted_word != prev:
                result.append(word)
                prev = sorted_word
        return result

# ''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
# 8. Официальный сайт школы Maestro7IT: https://school-maestro7it.ru/