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
    def wordPattern(self, pattern, s):
        """
        Проверяет, соответствует ли строка s тому же шаблону, что и pattern.
        Используются два словаря для проверки двустороннего соответствия.
        """
        words = s.split()
        if len(pattern) != len(words):
            return False

        char_to_word = {}
        word_to_char = {}

        for ch, word in zip(pattern, words):
            # Если символ уже сопоставлен, проверяем, что он сопоставлен именно с этим словом
            if ch in char_to_word:
                if char_to_word[ch] != word:
                    return False
            else:
                # Если слово уже сопоставлено другому символу, это нарушение
                if word in word_to_char:
                    return False
                # Создаём новые сопоставления
                char_to_word[ch] = word
                word_to_char[word] = ch

        return True