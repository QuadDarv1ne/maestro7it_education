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
    def processStr(self, s, k):
        """
        Возвращает k-й символ (0-индексация) строки, полученной после обработки s.

        Правила обработки s слева направо:
        - Строчная буква: добавляется в конец result.
        - '*': удаляет последний символ result, если он есть.
        - '#': дублирует result (result = result + result).
        - '%': переворачивает result.

        Поскольку k может достигать 10^15, прямое построение строки невозможно.
        Алгоритм:
        1. Прямой проход: вычисляем длину result после каждой операции.
        2. Если k >= итоговой длины, возвращаем '.'.
        3. Обратный проход с отслеживанием позиции p и флага переворота r.
           Флаг r позволяет обрабатывать '%' без точного значения длины:
           при '%' просто инвертируем r, не вычисляя L[i] - 1 - p.

        Ограничения: 1 <= len(s) <= 10^5, 0 <= k <= 10^15.
        Промежуточная длина не превышает 10^15 + |s| (каждая '*' убирает
        максимум один символ; чтобы после '#' вернуться к <= 10^15, нужно
        больше '*', чем есть в s), что помещается в 64-битное целое.

        Сложность: время O(n), память O(n), где n = len(s).

        Примеры:
        >>> processStr("a#b%*", 1)
        'a'
        >>> processStr("cd%#*#", 3)
        'd'
        >>> processStr("z*#", 0)
        '.'
        """
        n = len(s)
        # L[i] — длина result после обработки s[0..i-1]. L[0] = 0.
        L = [0] * (n + 1)
        for i, c in enumerate(s):
            if c == '*':
                L[i + 1] = max(0, L[i] - 1)
            elif c == '#':
                L[i + 1] = L[i] * 2
            elif c == '%':
                L[i + 1] = L[i]
            else:
                L[i + 1] = L[i] + 1

        if k >= L[n]:
            return '.'

        p = k
        r = False
        for i in range(n - 1, -1, -1):
            c = s[i]
            if c == '*':
                if r:
                    p += 1
            elif c == '#':
                half = L[i]
                if p >= half:
                    p -= half
            elif c == '%':
                r = not r
            else:
                # Строчная буква
                if not r:
                    if p == L[i + 1] - 1:
                        return c
                else:
                    if p == 0:
                        return c
                    p -= 1
        return '.'