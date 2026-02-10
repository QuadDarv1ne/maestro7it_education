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
    def numberToWords(self, num):
        """
        Преобразует неотрицательное целое число в его словесное представление на английском языке.
        
        Args:
            num (int): Число от 0 до 2^31 - 1 (2 147 483 647)
            
        Returns:
            str: Словесное представление числа с заглавной буквы
            
        Examples:
            >>> numberToWords(123)
            "One Hundred Twenty Three"
            >>> numberToWords(1234567)
            "One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven"
            
        Approach:
            - Используем словари для базовых чисел и разрядных групп
            - Разбиваем число на группы по 3 цифры (тысячи, миллионы, миллиарды)
            - Каждую группу обрабатываем рекурсивно/итеративно
            - Особый случай: число 0
        """
        # Базовые словари
        ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", 
                "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", 
                "Seventeen", "Eighteen", "Nineteen"]
        tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
        thousands = ["", "Thousand", "Million", "Billion"]
        
        # Случай с нулем
        if num == 0:
            return "Zero"
        
        def helper(n):
            """Обрабатывает число меньше 1000"""
            if n == 0:
                return ""
            elif n < 20:
                return ones[n] + " "
            elif n < 100:
                return tens[n // 10] + " " + helper(n % 10)
            else:
                return ones[n // 100] + " Hundred " + helper(n % 100)
        
        result = ""
        i = 0
        
        while num > 0:
            if num % 1000 != 0:
                # Обрабатываем текущую группу из 3 цифр и добавляем разряд
                result = helper(num % 1000).strip() + " " + thousands[i] + " " + result
            num //= 1000
            i += 1
        
        return result.strip()