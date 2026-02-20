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

class Solution:
    def countBinarySubstrings(self, s):
        """
        Подсчитывает количество специальных подстрок в двоичной строке.

        Аргументы:
            s (str): Бинарная строка, состоящая только из '0' и '1'.

        Возвращает:
            int: Количество подстрок с равным числом сгруппированных 0 и 1.

        Пример:
            >>> Solution().countBinarySubstrings("00110011")
            6
        """
        prev_count = 0  # Длина предыдущей группы
        curr_count = 1  # Длина текущей группы
        result = 0

        for i in range(1, len(s)):
            if s[i] == s[i - 1]:
                curr_count += 1  # Продолжаем текущую группу
            else:
                # Переход к новой группе — добавляем минимум
                result += min(prev_count, curr_count)
                prev_count = curr_count
                curr_count = 1

        # Учитываем последнюю пару групп
        result += min(prev_count, curr_count)
        return result