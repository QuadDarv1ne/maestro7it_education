"""
Разделение квадратов горизонтальной линией

@param squares Массив квадратов [x, y, длина]
@return Минимальная y-координата разделяющей линии

Сложность: Время O(n log max_y), Память O(1)

Автор: Дуплей Максим Игоревич
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
    def separateSquares(self, squares):
        # Вычисление общей площади всех квадратов
        total_area = sum(l * l for _, _, l in squares)
        target_area = total_area / 2.0
        
        # Определение диапазона поиска
        low = 0.0
        high = max(y + l for _, y, l in squares)
        
        # Функция для вычисления площади ниже линии y
        def area_below(y_line):
            area = 0.0
            for _, y, l in squares:
                if y >= y_line:
                    # Квадрат полностью выше линии
                    continue
                elif y + l <= y_line:
                    # Квадрат полностью ниже линии
                    area += l * l
                else:
                    # Квадрат пересекает линию
                    height = y_line - y
                    area += height * l
            return area
        
        # Бинарный поиск с фиксированным числом итераций для точности
        for _ in range(100):
            mid = (low + high) / 2.0
            if area_below(mid) < target_area:
                low = mid
            else:
                high = mid
        
        return low