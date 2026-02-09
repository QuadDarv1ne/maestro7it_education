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
    def countDigitOne(self, n):
        """
        Подсчитывает количество цифр 1 во всех числах от 1 до n.
        
        Алгоритм:
        Для каждого разряда (единицы, десятки, сотни и т.д.) вычисляем, сколько раз
        цифра 1 появляется в этом разряде при записи чисел от 1 до n.
        
        Формула для разряда, соответствующего 10^k:
        - high = n // (10^(k+1))
        - low = n % (10^k)
        - cur = (n // (10^k)) % 10
        
        Количество единиц в этом разряде:
        count = high * (10^k) + 
                если cur > 1: добавляем 10^k
                если cur == 1: добавляем low + 1
                если cur == 0: добавляем 0
        
        Сложность:
        Время: O(log10(n)) - проходим по каждому разряду числа
        Пространство: O(1) - используем только константную память
        
        Параметры:
        ----------
        n : int
            Верхняя граница диапазона чисел
            
        Возвращает:
        -----------
        int
            Общее количество цифр 1 во всех числах от 1 до n
            
        Примеры:
        --------
        countDigitOne(13) → 6
        Объяснение: Цифра 1 встречается в числах: 1, 10, 11, 12, 13.
        В 11 две единицы, итого: 1 + 1 + 1 + 1 + 1 + 1 = 6
        
        countDigitOne(0) → 0
        countDigitOne(113) → 40
        """
        if n <= 0:
            return 0
        
        count = 0
        factor = 1  # Текущий разряд: 1, 10, 100, ...
        
        while factor <= n:
            # Вычисляем high, low, cur для текущего разряда
            high = n // (factor * 10)
            low = n % factor
            cur = (n // factor) % 10
            
            # Добавляем базовую часть: high * factor
            count += high * factor
            
            # Добавляем дополнительную часть в зависимости от cur
            if cur > 1:
                count += factor
            elif cur == 1:
                count += low + 1
            # Если cur == 0, ничего не добавляем
            
            # Переходим к следующему разряду
            factor *= 10
        
        return count
    
    def countDigitOne_bruteforce(self, n):
        """
        Наивное решение для проверки (неэффективно для больших n).
        
        Параметры:
        ----------
        n : int
            Верхняя граница диапазона
            
        Возвращает:
        -----------
        int
            Количество цифр 1
        """
        count = 0
        for i in range(1, n + 1):
            num = i
            while num > 0:
                if num % 10 == 1:
                    count += 1
                num //= 10
        return count