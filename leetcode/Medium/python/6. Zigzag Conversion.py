'''
https://leetcode.com/problems/zigzag-conversion/description/
'''

class Solution:
    def convert(self, s, numRows):
        """
        Преобразует строку s в зигзагообразный паттерн с numRows строками.
        """
        if numRows == 1 or numRows >= len(s):
            return s
        
        rows = [''] * numRows
        currentRow = 0
        goingDown = False

        for c in s:
            rows[currentRow] += c
            if currentRow == 0 or currentRow == numRows - 1:
                goingDown = not goingDown
            currentRow += 1 if goingDown else -1

        return ''.join(rows)

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks