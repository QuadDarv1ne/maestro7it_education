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

Проверяет, можно ли сделать две строки длины 4 равными,
меняя местами символы на позициях, разница между которыми равна 2.

Параметры:
    s1 (str): первая строка
    s2 (str): вторая строка

Возвращает:
    bool: True, если строки можно сделать равными, иначе False

Примечания:
    - Длина строк равна 4
    - Доступны только два возможных обмена: (0,2) и (1,3)
    - Сложность: O(1) по времени и памяти
"""

class Solution(object):
    def canBeEqual(self, s1, s2):
        """
        :type s1: str
        :type s2: str
        :rtype: bool
        """
        # Сравниваем символы на чётных позициях (0 и 2)
        if sorted([s1[0], s1[2]]) != sorted([s2[0], s2[2]]):
            return False
        
        # Сравниваем символы на нечётных позициях (1 и 3)
        if sorted([s1[1], s1[3]]) != sorted([s2[1], s2[3]]):
            return False
        
        return True