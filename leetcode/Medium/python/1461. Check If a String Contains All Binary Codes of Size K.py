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
    def hasAllCodes(self, s, k):
        """
        Проверяет, содержит ли строка s все бинарные коды длины k.
        
        Алгоритм:
        - Минимально необходимая длина строки: 2^k + k - 1.
        - Проходим по строке окном длины k, добавляем каждую подстроку в множество.
        - Если в конце размер множества равен 2^k, возвращаем True.
        
        Аргументы:
            s: входная бинарная строка
            k: длина кода
            
        Returns:
            True, если все коды присутствуют, иначе False
        """
        need = 1 << k          # 2^k
        if len(s) < need + k - 1:
            return False
        
        seen = set()
        for i in range(len(s) - k + 1):
            seen.add(s[i:i+k])
            if len(seen) == need:  # ранний выход, если набрали все
                return True
        return len(seen) == need