'''
https://leetcode.com/problems/longest-substring-without-repeating-characters/description/
'''

class Solution:
    def lengthOfLongestSubstring(self, s):
        """
        Находит длину самой длинной подстроки без повторяющихся символов.

        Алгоритм:
        - Метод скользящего окна (sliding window).
        - last_seen хранит последний индекс появления символа (или -1, если не встречался).
        - j — индекс перед началом текущего окна.
        - Для каждого символа s[i]:
            * Если символ встречался, сдвигаем j вправо: j = max(j, last_seen[символ]).
            * Вычисляем длину окна: i - j.
            * Обновляем максимум.
            * Запоминаем индекс текущего символа.
        Сложность:
        - Время: O(n)
        - Память: O(1) для фиксированного алфавита ASCII.
        
        :param s: входная строка
        :return: длина самой длинной подстроки без повторов
        """
        last_seen = {}
        ans = 0
        j = -1
        for i, c in enumerate(s):
            if c in last_seen:
                j = max(j, last_seen[c])
            ans = max(ans, i - j)
            last_seen[c] = i
        return ans

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks