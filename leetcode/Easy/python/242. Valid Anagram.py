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
    def isAnagram(self, s, t):
        """
        Проверяет, является ли строка t анаграммой строки s.
        
        Алгоритм (подсчет символов):
        1. Если длины строк не равны, возвращаем False.
        2. Создаем массив/словарь для подсчета частот символов.
        3. Увеличиваем счетчики для символов строки s.
        4. Уменьшаем счетчики для символов строки t.
        5. Если все счетчики равны 0, строки являются анаграммами.
        
        Сложность:
        Время: O(n), где n - длина строк (проходим по каждой строке один раз)
        Пространство: O(1) или O(k), где k - размер алфавита (26 для английских букв)
        
        Параметры:
        ----------
        s : str
            Первая строка
        t : str
            Вторая строка
            
        Возвращает:
        -----------
        bool
            True, если t является анаграммой s, иначе False
            
        Примеры:
        --------
        isAnagram("anagram", "nagaram") → True
        isAnagram("rat", "car") → False
        isAnagram("", "") → True
        """
        # Если длины строк разные, они не могут быть анаграммами
        if len(s) != len(t):
            return False
        
        # Вариант 1: Использование массива (оптимально для английских букв)
        char_count = [0] * 26  # 26 букв английского алфавита
        
        for char in s:
            char_count[ord(char) - ord('a')] += 1
        
        for char in t:
            index = ord(char) - ord('a')
            char_count[index] -= 1
            # Если счетчик стал отрицательным, значит в t больше этого символа
            if char_count[index] < 0:
                return False
        
        # Проверяем, что все счетчики равны 0
        return all(count == 0 for count in char_count)
    
    def isAnagram_counter(self, s, t):
        """
        Решение с использованием Counter из collections.
        
        Параметры:
        ----------
        s : str
            Первая строка
        t : str
            Вторая строка
            
        Возвращает:
        -----------
        bool
            True, если строки являются анаграммами
        """
        from collections import Counter
        return Counter(s) == Counter(t)
    
    def isAnagram_sort(self, s, t):
        """
        Решение с использованием сортировки.
        
        Сложность:
        Время: O(n log n) из-за сортировки
        Пространство: O(n) (или O(1) в зависимости от реализации сортировки)
        
        Параметры:
        ----------
        s : str
            Первая строка
        t : str
            Вторая строка
            
        Возвращает:
        -----------
        bool
            True, если строки являются анаграммами
        """
        return sorted(s) == sorted(t)