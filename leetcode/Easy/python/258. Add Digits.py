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
    def addDigits(self, num):
        """
        Вычисляет цифровой корень числа (рекурсивную сумму цифр до одной цифры).
        
        Алгоритм 1 (математический):
        Цифровой корень числа num можно вычислить по формуле:
        - Если num == 0: возвращаем 0
        - Иначе: 1 + (num - 1) % 9
        
        Алгоритм 2 (итеративный):
        1. Пока число имеет более одной цифры:
           - Складываем все его цифры
           - Заменяем число на сумму цифр
        2. Возвращаем полученную одну цифру
        
        Сложность:
        Математический: O(1) по времени, O(1) по памяти
        Итеративный: O(log n) по времени, O(1) по памяти
        
        Параметры:
        ----------
        num : int
            Исходное число
            
        Возвращает:
        -----------
        int
            Цифровой корень числа (одна цифра)
            
        Примеры:
        --------
        addDigits(38) → 2
        Объяснение: 3 + 8 = 11, 1 + 1 = 2
        
        addDigits(0) → 0
        addDigits(9) → 9
        addDigits(123) → 6 (1+2+3=6)
        """
        # Математический подход (цифровой корень)
        if num == 0:
            return 0
        return 1 + (num - 1) % 9
    
    def addDigits_iterative(self, num):
        """
        Итеративное решение.
        
        Параметры:
        ----------
        num : int
            Исходное число
            
        Возвращает:
        -----------
        int
            Цифровой корень
        """
        while num >= 10:
            # Суммируем цифры текущего числа
            digit_sum = 0
            while num > 0:
                digit_sum += num % 10  # Добавляем последнюю цифру
                num //= 10  # Удаляем последнюю цифру
            num = digit_sum
        return num
    
    def addDigits_recursive(self, num):
        """
        Рекурсивное решение.
        
        Параметры:
        ----------
        num : int
            Исходное число
            
        Возвращает:
        -----------
        int
            Цифровой корень
        """
        if num < 10:
            return num
        
        # Суммируем цифры
        digit_sum = 0
        while num > 0:
            digit_sum += num % 10
            num //= 10
        
        # Рекурсивно вызываем для суммы
        return self.addDigits_recursive(digit_sum)