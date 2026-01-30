'''
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
    def reverseWords(self, s):
        """
        Разворачивает порядок слов в строке.
        
        Параметры:
        s (str): Исходная строка, которая может содержать лишние пробелы.
        
        Возвращает:
        str: Строка с обратным порядком слов, где слова разделены одним пробелом.
        
        Примеры:
        >>> reverseWords("the sky is blue")
        "blue is sky the"
        >>> reverseWords("  hello world  ")
        "world hello"
        >>> reverseWords("a good   example")
        "example good a"
        
        Алгоритм:
        1. Удаляем лишние пробелы в начале и конце строки
        2. Разбиваем строку на слова (метод split() без параметров обрабатывает множественные пробелы)
        3. Разворачиваем список слов
        4. Соединяем слова обратно через один пробел
        
        Примечания:
        - В Python строки неизменяемы, поэтому создается новая строка
        - Временная сложность: O(n), где n - длина строки
        - Пространственная сложность: O(n) для хранения списка слов
        """
        # Удаляем пробелы по краям
        s = s.strip()
        
        # Разбиваем на слова (множественные пробелы игнорируются)
        words = s.split()
        
        # Разворачиваем порядок слов
        words.reverse()
        
        # Соединяем слова через один пробел
        return ' '.join(words)