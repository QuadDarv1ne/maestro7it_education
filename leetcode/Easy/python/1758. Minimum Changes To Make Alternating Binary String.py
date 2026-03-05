'''
https://leetcode.com/problems/add-binary/description/
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
'''

class Solution:
    def minOperations(self, s):
        """
        Возвращает минимальное количество изменений символов,
        чтобы строка стала чередующейся (соседние символы различны).

        Алгоритм:
        - Существует только два возможных чередующихся паттерна для данной длины:
          начинающийся с '0' (0,1,0,1,...) и начинающийся с '1' (1,0,1,0,...).
        - Считаем количество несовпадений исходной строки с каждым паттерном.
        - Ответ — минимум из двух полученных значений.

        Параметры:
        s (str): Исходная строка из символов '0' и '1'.

        Возвращает:
        int: Минимальное количество операций замены.
        """
        n = len(s)
        count1 = 0  # несовпадения с паттерном, начинающимся с '0'
        count2 = 0  # несовпадения с паттерном, начинающимся с '1'

        for i, ch in enumerate(s):
            # Паттерн1: на чётных позициях должен быть '0', на нечётных — '1'
            if i % 2 == 0 and ch != '0':
                count1 += 1
            if i % 2 == 1 and ch != '1':
                count1 += 1

            # Паттерн2: на чётных позициях должен быть '1', на нечётных — '0'
            if i % 2 == 0 and ch != '1':
                count2 += 1
            if i % 2 == 1 and ch != '0':
                count2 += 1

        return min(count1, count2)