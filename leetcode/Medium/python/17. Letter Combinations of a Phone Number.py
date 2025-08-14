'''
https://leetcode.com/problems/letter-combinations-of-a-phone-number/description/
'''

class Solution:
    def letterCombinations(self, digits):
        """
        Возвращает все возможные комбинации букв для заданной строки digits.
        """
        if not digits:
            return []

        digit_map = {
            '2': 'abc', '3': 'def', '4': 'ghi',
            '5': 'jkl', '6': 'mno', '7': 'pqrs',
            '8': 'tuv', '9': 'wxyz'
        }

        def backtrack(index, current):
            if index == len(digits):
                combinations.append(current)
                return
            for letter in digit_map[digits[index]]:
                backtrack(index + 1, current + letter)

        combinations = []
        backtrack(0, "")
        return combinations

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks