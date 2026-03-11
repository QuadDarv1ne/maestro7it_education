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
    """
    Решение задачи «Дополнение до 10 целого числа».
    
    Алгоритм: Битовая инверсия с помощью маски.
    
    Идея:
        - Найти количество бит в числе n: bit_length
        - Создать маску из всех единиц: mask = (1 << bit_length) - 1
        - Инвертировать биты числа: result = n ^ mask
    
    Особый случай:
        - Если n == 0, возвращаем 1 (дополнение 0 → 1)
    
    Пример:
        n = 5 (бинарно: 101)
        bit_length = 3
        mask = (1 << 3) - 1 = 7 (бинарно: 111)
        result = 5 ^ 7 = 2 (бинарно: 010) ✓
    
    Сложность:
        Время: O(1) — фиксированное количество бит (≤30)
        Память: O(1)
    """
    
    def bitwiseComplement(self, n):
        # Особый случай: дополнение 0 равно 1
        if n == 0:
            return 1
        
        # Находим количество бит в числе
        bit_length = n.bit_length()
        
        # Создаём маску из всех единиц нужной длины
        # Пример: для 3 бит → 111 (бинарно) = 7 (десятично)
        mask = (1 << bit_length) - 1
        
        # XOR инвертирует все биты числа в пределах маски
        return n ^ mask