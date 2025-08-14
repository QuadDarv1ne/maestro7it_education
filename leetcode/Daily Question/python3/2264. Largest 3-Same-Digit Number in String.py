'''
https://leetcode.com/problems/largest-3-same-digit-number-in-string/description/?envType=daily-question&envId=2025-08-14
'''

class Solution:
    def largestGoodInteger(self, num: str) -> str:
        """
        Находит наибольшее "хорошее" число в строке.
        "Хорошее" число — это подстрока длиной 3 с одинаковыми символами.

        Алгоритм:
        1. Перебираем цифры от 9 до 0.
        2. Строим строку из трёх одинаковых цифр.
        3. Проверяем, встречается ли она в num.
        4. Первое найденное совпадение — ответ.
        """
        for d in range(9, -1, -1):
            t = str(d) * 3
            if t in num:
                return t
        return ""

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks