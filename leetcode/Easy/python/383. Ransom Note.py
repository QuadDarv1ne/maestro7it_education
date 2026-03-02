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
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        """
        Определяет, можно ли составить строку ransomNote из букв magazine.
        Каждая буква из magazine может использоваться только один раз.

        Алгоритм:
        1. Создаём массив счётчиков для 26 букв.
        2. Учитываем все буквы из magazine (увеличиваем счётчики).
        3. Проверяем, хватает ли букв для ransomNote (уменьшаем счётчики).

        Аргументы:
            ransomNote (str): строка, которую нужно составить.
            magazine (str): строка с доступными буквами.

        Возвращает:
            bool: True, если составить можно, иначе False.
        """
        # Массив для подсчёта букв от 'a' до 'z'
        count = [0] * 26

        # Подсчитываем все буквы в magazine
        for ch in magazine:
            count[ord(ch) - ord('a')] += 1

        # Проверяем, хватает ли букв для ransomNote
        for ch in ransomNote:
            index = ord(ch) - ord('a')
            count[index] -= 1
            if count[index] < 0:
                return False

        return True