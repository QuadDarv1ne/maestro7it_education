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
    def nextGreatestLetter(self, letters, target):
        """
        Находит наименьший символ в отсортированном списке, который больше заданного целевого символа.

        Если в списке нет символов, больших целевого, функция возвращает первый символ списка
        (происходит "заворачивание" по кругу).

        Параметры:
        letters : list
            Отсортированный список символов в порядке неубывания.
            Содержит как минимум два различных символа.
        target : str
            Целевой символ, для которого ищется ближайший больший символ.

        Возвращает:
        str
            Наименьший символ из letters, который больше target.
            Если такого символа нет, возвращается letters[0].

        Примеры:
        >>> Solution().nextGreatestLetter(["c", "f", "j"], "a")
        'c'
        >>> Solution().nextGreatestLetter(["c", "f", "j"], "c")
        'f'
        >>> Solution().nextGreatestLetter(["c", "f", "j"], "z")
        'c'
        """
        n = len(letters)
        left, right = 0, n - 1
        
        while left <= right:
            mid = left + (right - left) // 2
            if letters[mid] <= target:
                left = mid + 1
            else:
                right = mid - 1
        
        return letters[left] if left < n else letters[0]