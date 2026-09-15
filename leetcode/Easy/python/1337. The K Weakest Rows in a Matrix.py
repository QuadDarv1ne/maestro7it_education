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
    def kWeakestRows(self, mat, k):
        """
        Возвращает индексы k самых слабых строк бинарной матрицы.

        Алгоритм:
        1. Для каждой строки считаем количество солдат (единиц) через .count(1).
        2. Сортируем строки по (количество_солдат, индекс).
        3. Берём первые k индексов.

        Параметры:
        mat (list[list[int]]) – матрица m x n из 0 и 1.
        k (int) – количество слабейших строк.

        Возвращает:
        list[int] – индексы строк (от самой слабой к более сильной).
        """
        # Собираем пары (количество_солдат, индекс_строки)
        strength = []
        for i, row in enumerate(mat):
            soldiers = row.count(1)   # можно заменить на бинарный поиск для скорости
            strength.append((soldiers, i))
        # Сортируем (по умолчанию сначала по первому элементу, потом по второму)
        strength.sort()
        # Извлекаем индексы и возвращаем первые k
        return [idx for _, idx in strength[:k]]