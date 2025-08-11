'''
https://leetcode.com/problems/minimum-window-substring/description/?envType=study-plan-v2&envId=top-interview-150
'''

from collections import Counter

class Solution:
    def minWindow(self, s, t):
        """
        Находит минимальную подстроку в s, содержащую все символы из t (с учётом количества).

        Параметры:
        ----------
        s : str
            Исходная строка.
        t : str
            Строка с требуемыми символами.

        Возвращаемое значение:
        ----------------------
        str
            Минимальная подстрока s, содержащая все символы t. Пустая строка, если нет решения.

        Алгоритм:
        ---------
        Используем два указателя и словарь счетчиков:
        - count_t хранит количество каждого символа в t,
        - count_window — количество символов в текущем окне,
        - formed — сколько уникальных символов удовлетворяют условие по количеству,
        - пытаемся расширять и сужать окно, чтобы найти минимальное.
        """
        if not t or not s:
            return ""

        dict_t = Counter(t)
        required = len(dict_t)

        left, right = 0, 0
        formed = 0
        window_counts = {}

        ans = float("inf"), None, None  # длина, левый, правый

        while right < len(s):
            character = s[right]
            window_counts[character] = window_counts.get(character, 0) + 1

            if character in dict_t and window_counts[character] == dict_t[character]:
                formed += 1

            while left <= right and formed == required:
                character = s[left]

                # Обновляем ответ
                if right - left + 1 < ans[0]:
                    ans = (right - left + 1, left, right)

                window_counts[character] -= 1
                if character in dict_t and window_counts[character] < dict_t[character]:
                    formed -= 1

                left += 1

            right += 1

        return "" if ans[0] == float("inf") else s[ans[1]:ans[2] + 1]

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks