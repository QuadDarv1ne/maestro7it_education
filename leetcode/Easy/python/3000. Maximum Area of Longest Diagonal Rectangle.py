'''
https://leetcode.com/problems/maximum-area-of-longest-diagonal-rectangle/description/?envType=daily-question&envId=2025-08-26

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

class Solution:
    def areaOfMaxDiagonal(self, dimensions):
        """
        Определение максимальной площади прямоугольника с самой длинной диагональю.

        Алгоритм:
        1. Для каждого прямоугольника считаем квадрат диагонали: diag_sq = l*l + w*w.
        2. Сравниваем diag_sq с текущим максимумом:
           - Если diag_sq больше, обновляем и диагональ, и площадь.
           - Если diag_sq равен максимуму, выбираем больший из вариантов по площади.
        3. Возвращаем площадь прямоугольника с максимальной диагональю.

        :param dimensions: Список прямоугольников в формате [длина, ширина]
        :return: Площадь подходящего прямоугольника
        """
        max_diag_sq = max_area = 0
        for l, w in dimensions:
            diag_sq = l*l + w*w
            area = l*w
            if diag_sq > max_diag_sq:
                max_diag_sq, max_area = diag_sq, area
            elif diag_sq == max_diag_sq:
                max_area = max(max_area, area)
        return max_area

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks