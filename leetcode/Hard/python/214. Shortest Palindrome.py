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
    def shortestPalindrome(self, s):
        """
        Находит кратчайший палиндром, добавляя символы в начало строки.
        
        Алгоритм:
        1. Найти самый длинный палиндромный префикс в строке
        2. Перевернуть оставшийся суффикс и добавить в начало
        
        Используется алгоритм КМП для нахождения самого длинного префикса,
        который является палиндромом.
        
        Сложность: O(n) время, O(n) память
        """
        
        # Если строка пустая или уже палиндром
        if not s:
            return s
        
        # Создаем строку для поиска палиндромного префикса
        # Формат: s + "#" + reverse(s)
        rev_s = s[::-1]
        combined = s + "#" + rev_s
        
        # Вычисляем префикс-функцию (массив pi) для комбинированной строки
        n = len(combined)
        pi = [0] * n
        
        # Вычисление префикс-функции
        for i in range(1, n):
            j = pi[i - 1]
            
            # Пока есть несовпадение, отступаем назад
            while j > 0 and combined[i] != combined[j]:
                j = pi[j - 1]
            
            # Если символы совпадают, увеличиваем j
            if combined[i] == combined[j]:
                j += 1
            
            pi[i] = j
        
        # Длина самого длинного палиндромного префикса
        # Это последнее значение в массиве pi
        longest_palindrome_prefix = pi[-1]
        
        # Часть, которую нужно добавить в начало
        to_add = rev_s[:len(s) - longest_palindrome_prefix]
        
        return to_add + s