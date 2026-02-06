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

from functools import cmp_to_key
# from typing import List

class Solution:
    def largestNumber(self, nums):
        # Преобразуем числа в строки для сравнения конкатенаций
        str_nums = list(map(str, nums))
        
        # Кастомный компаратор для сортировки
        def compare(x, y):
            # Сравниваем x+y и y+x
            if x + y > y + x:
                return -1  # x должно идти первым
            elif x + y < y + x:
                return 1   # y должно идти первым
            else:
                return 0
        
        # Сортируем с использованием кастомного компаратора
        str_nums.sort(key=cmp_to_key(compare))
        
        # Собираем результат
        result = ''.join(str_nums)
        
        # Обрабатываем случай с ведущими нулями
        return result if result[0] != '0' else '0'