'''
LeetCode 1653. Minimum Deletions to Make String Balanced
https://leetcode.com/problems/minimum-deletions-to-make-string-balanced/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. YouTube канал: https://www.youtube.com/@it-coders
6. ВК группа: https://vk.com/science_geeks
'''

class Solution:
    def minimumDeletions(self, s):
        """
        Находит минимальное количество удалений символов для получения сбалансированной строки.
        
        Сбалансированной считается строка, в которой все буквы 'a' находятся перед всеми буквами 'b',
        то есть строка не содержит подстроки "ba".
        
        Параметры:
        -----------
        s : str
            Входная строка, состоящая только из символов 'a' и 'b'.
            
        Возвращает:
        -----------
        int
            Минимальное количество удалений символов, необходимых для получения сбалансированной строки.
            
        Алгоритм:
        ---------
        1. Подсчитываем общее количество букв 'a' в строке.
        2. Проходим по строке, поддерживая:
           - left_b: количество 'b' слева от текущей позиции
           - right_a: количество 'a' справа от текущей позиции
        3. На каждом шаге рассматриваем разрез строки в текущей позиции:
           - Удаляем все 'b' слева (left_b)
           - Удаляем все 'a' справа (right_a)
        4. Минимизируем сумму left_b + right_a по всем позициям.
        
        Сложность:
        ----------
        - Время: O(n), один проход по строке
        - Память: O(1), используются только константные переменные
        
        Пример:
        -------
        >>> solution = Solution()
        >>> solution.minimumDeletions("aababbab")
        2
        >>> solution.minimumDeletions("bbaaaaabb")
        2
        >>> solution.minimumDeletions("a")
        0
        """
        total_a = s.count('a')
        left_b = 0
        right_a = total_a
        min_deletions = left_b + right_a  # разрез перед первым символом
        
        for ch in s:
            if ch == 'a':
                right_a -= 1
            else:  # ch == 'b'
                left_b += 1
            deletions = left_b + right_a
            if deletions < min_deletions:
                min_deletions = deletions
        
        return min_deletions