class Solution:
    def partition(self, s):
        """
        Находит все возможные разбиения строки на палиндромные подстроки.
        
        Алгоритм:
        1. Используем backtracking для генерации всех возможных разбиений
        2. Проверяем каждый префикс на палиндромность
        3. Рекурсивно обрабатываем оставшуюся часть строки
        
        Сложность: O(n * 2^n) время, O(n) память
        
        Пример:
        Вход: "aab" -> [["a","a","b"], ["aa","b"]]
        Вход: "a" -> [["a"]]

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
        
        result = []
        
        def is_palindrome(sub):
            """Проверяет, является ли строка палиндромом."""
            return sub == sub[::-1]
        
        def backtrack(start, path):
            """
            Рекурсивно генерирует все возможные разбиения.
            
            Параметры:
            start: начальный индекс текущей подстроки
            path: текущий путь разбиения
            """
            # Если дошли до конца строки, добавляем текущий путь в результат
            if start == len(s):
                result.append(path[:])
                return
            
            # Перебираем все возможные окончания текущей подстроки
            for end in range(start + 1, len(s) + 1):
                # Берем текущую подстроку
                substring = s[start:end]
                
                # Если подстрока - палиндром, продолжаем рекурсию
                if is_palindrome(substring):
                    path.append(substring)  # Добавляем подстроку в путь
                    backtrack(end, path)    # Рекурсивно обрабатываем остаток
                    path.pop()              # Удаляем подстроку (backtrack)
        
        backtrack(0, [])
        return result