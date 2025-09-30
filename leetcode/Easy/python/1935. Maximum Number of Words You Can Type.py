'''
https://leetcode.com/problems/maximum-number-of-words-you-can-type/description/?envType=daily-question&envId=2025-09-15

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

class Solution:
    def canBeTypedWords(self, text, brokenLetters):
        """
        Подсчитывает количество слов в тексте, которые можно набрать, не используя сломанные клавиши.

        Параметры:
        text (str): Исходный текст, разделенный пробелами.
        brokenLetters (str): Строка с символами сломанных клавиш.

        Возвращает:
        int: Количество слов, которые можно набрать без использования сломанных клавиш.
        """
        words = text.split()
        count = 0
        for word in words:
            if all(char not in brokenLetters for char in word):
                count += 1
        return count

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks