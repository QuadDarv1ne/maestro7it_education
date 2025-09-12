'''
https://leetcode.com/problems/vowels-game-in-a-string/description/?envType=daily-question&envId=2025-09-12
'''

class Solution:
    def doesAliceWin(self, s):
        """
        Проверяет, выиграет ли Alice при оптимальной игре.
        Возвращает True, если в строке есть хотя бы одна гласная, иначе False.
        """
        for c in s:
            if c in "aeiou":
                return True
        return False

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks