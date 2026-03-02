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
    def findTheDifference(self, s: str, t: str) -> str:
        """
        Находит добавленный символ в строке t по сравнению с s.
        Использует XOR для объединения всех символов — парные сократятся,
        останется только добавленный символ.

        Аргументы:
            s (str): исходная строка.
            t (str): строка после перемешивания с добавлением одного символа.

        Возвращает:
            str: добавленный символ.
        """
        result = 0
        # XOR всех символов из s
        for ch in s:
            result ^= ord(ch)
        # XOR всех символов из t
        for ch in t:
            result ^= ord(ch)
        # Результат — ASCII-код добавленного символа
        return chr(result)