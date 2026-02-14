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
    def champagneTower(self, poured: int, query_row: int, query_glass: int) -> float:
        # Текущий ряд (начинаем с верхнего стакана)
        current_row = [float(poured)]

        for row in range(query_row):
            # Следующий ряд будет иметь на один стакан больше
            next_row = [0.0] * (row + 2)

            for i, volume in enumerate(current_row):
                if volume > 1.0:
                    excess = (volume - 1.0) / 2.0
                    next_row[i] += excess
                    next_row[i + 1] += excess

            current_row = next_row

        # Индекс query_glass гарантированно существует в current_row
        return min(1.0, current_row[query_glass])
    