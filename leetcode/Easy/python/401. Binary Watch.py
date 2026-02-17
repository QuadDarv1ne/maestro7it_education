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

class Solution(object):
    def readBinaryWatch(self, turnedOn):
        """
        Возвращает все возможные времена, которые могут показывать бинарные часы,
        при заданном количестве горящих светодиодов.

        :type turnedOn: int
        :rtype: List[str]
        """
        result = []
        for hour in range(12):
            for minute in range(60):
                # Подсчёт количества единичных битов в часе и минуте
                if (bin(hour).count('1') + bin(minute).count('1')) == turnedOn:
                    # Форматирование: часы без ведущего нуля, минуты всегда две цифры
                    result.append("{}:{:02d}".format(hour, minute))
        return result