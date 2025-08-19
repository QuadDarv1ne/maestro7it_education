'''
https://leetcode.com/problems/integer-to-roman/description/
'''

class Solution:
    def intToRoman(self, num):
        """
        Преобразует целое число (1 ≤ num ≤ 3999) в римское число.

        Подход:
        - Используется жадный алгоритм: проходим по списку (value, symbol) 
          от большего к меньшему.
        - Пока num >= value, вычитаем value и добавляем symbol в результат.
        - Итоговая строка — римское представление.
        """
        value_symbols = [
            (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
            (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
            (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
        ]
        roman = ""
        for value, symbol in value_symbols:
            while num >= value:
                roman += symbol
                num -= value
        return roman

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks