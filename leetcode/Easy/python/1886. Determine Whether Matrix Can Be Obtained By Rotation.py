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

"""
Определяет, можно ли получить целевую матрицу путем поворота исходной на 90°.

Параметры:
    mat (List[List[int]]): Исходная квадратная бинарная матрица.
    target (List[List[int]]): Целевая квадратная бинарная матрица.

Возвращает:
    bool: True, если можно получить target поворотами mat на 90°, иначе False.

Примечания:
    - Матрицы имеют размер n x n (1 <= n <= 10)
    - Элементы матриц: 0 или 1
    - Проверяются 4 возможных поворота: 0°, 90°, 180°, 270°
    - Сложность: O(n²) по времени, O(1) дополнительной памяти

Пример:
    >>> mat = [[0,1],[1,0]]
    >>> target = [[1,0],[0,1]]
    >>> findRotation(mat, target)
    True
"""

class Solution(object):
    def findRotation(self, mat, target):
        """
        Определяет, можно ли получить целевую матрицу путем поворота исходной.
        
        Аргументы:
            mat: исходная квадратная бинарная матрица
            target: целевая квадратная бинарная матрица
        
        Возвращает:
            True, если можно получить target поворотами mat на 90°, иначе False
        """
        n = len(mat)
        
        # Проверяем 4 возможных поворота (0°, 90°, 180°, 270°)
        for _ in range(4):
            if mat == target:
                return True
            # Поворачиваем mat на 90° по часовой стрелке
            mat = [list(row) for row in zip(*mat[::-1])]
        
        return False