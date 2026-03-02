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
    def isSubsequence(self, s: str, t: str) -> bool:
        """
        Проверяет, является ли s подпоследовательностью t.

        Алгоритм двух указателей:
        - i — индекс в s, j — индекс в t.
        - Двигаем j по t. При совпадении s[i] и t[j] сдвигаем i.
        - Если i дошёл до конца s — значит, все символы найдены по порядку.

        Аргументы:
            s: строка, которую проверяем на подпоследовательность.
            t: строка, в которой ищем.

        Возвращает:
            True, если s — подпоследовательность t, иначе False.
        """
        i, j = 0, 0
        while i < len(s) and j < len(t):
            if s[i] == t[j]:
                i += 1
            j += 1
        return i == len(s)