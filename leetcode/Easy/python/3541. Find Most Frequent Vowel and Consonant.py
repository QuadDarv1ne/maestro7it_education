'''
https://leetcode.com/problems/find-most-frequent-vowel-and-consonant/description/?envType=daily-question&envId=2025-09-13

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

class Solution:
    def maxFreqSum(self, s):
        """
        Задача: найти сумму частоты наиболее часто встречающейся
        гласной и частоты наиболее часто встречающейся согласной в строке s.

        Уточнения:
        - Рассматриваются только английские буквы 'a'..'z' (LeetCode передаёт нижний регистр).
        - Гласные: a, e, i, o, u.
        - Если гласных или согласных нет, их вклад равен 0.
        - Возвращается одно целое число: max_vowel_count + max_consonant_count.

        Сложность:
        - Время: O(n), где n = len(s).
        - Память: O(1) (массив фиксированного размера 26).
        """
        cnt = [0] * 26
        for ch in s:
            # на LeetCode s уже в нижнем регистре, но безопасно оставляем проверку
            if 'a' <= ch <= 'z':
                cnt[ord(ch) - 97] += 1
            else:
                c = ch.lower()
                if 'a' <= c <= 'z':
                    cnt[ord(c) - 97] += 1

        vowels = "aeiou"
        max_v = max(cnt[ord(v) - 97] for v in vowels)
        max_c = 0
        for i in range(26):
            ch = chr(97 + i)
            if ch in vowels:
                continue
            max_c = max(max_c, cnt[i])

        return max_v + max_c

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks