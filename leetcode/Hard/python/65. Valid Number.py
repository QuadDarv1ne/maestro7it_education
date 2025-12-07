class Solution:
    def isNumber(self, s):
        """
        Автор: Дуплей Максим Игоревич
        ORCID: https://orcid.org/0009-0007-7605-539X
        GitHub: https://github.com/QuadDarv1ne/
        
        Задача: Valid Number (LeetCode)
        Алгоритм: Валидация числа через конечный автомат (флаги)
        Сложность: O(n) по времени, O(1) по памяти
        
        Идея решения:
        1. Используем флаги для отслеживания: цифр, точки, экспоненты
        2. Проверяем каждый символ согласно правилам валидного числа
        3. Знак может быть только в начале или после 'e'/'E'
        4. Точка не может быть после 'e'/'E' или повторяться
        5. 'e'/'E' требует хотя бы одну цифру до себя
        """
        
        has_digit = False    # Есть ли цифры
        has_point = False    # Есть ли точка
        has_e = False        # Есть ли экспонента
        
        for i, c in enumerate(s):
            if c.isdigit():
                has_digit = True
            elif c == '.':
                # Точка не может быть после 'e' или повторяться
                if has_e or has_point:
                    return False
                has_point = True
            elif c in ['e', 'E']:
                # 'e' требует цифру до себя и не может повторяться
                if has_e or not has_digit:
                    return False
                has_e = True
                has_digit = False  # После 'e' должна быть хотя бы одна цифра
            elif c in ['+', '-']:
                # Знак только в начале или сразу после 'e'
                if i > 0 and s[i-1] not in ['e', 'E']:
                    return False
            else:
                # Недопустимый символ
                return False
        
        return has_digit


"""
Полезные ссылки автора:
Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
Telegram: @quadd4rv1n7, @dupley_maxim_1999
Rutube: https://rutube.ru/channel/4218729/
Plvideo: https://plvideo.ru/channel/AUPv_p1r5AQJ
YouTube: https://www.youtube.com/@it-coders
VK: https://vk.com/science_geeks
"""