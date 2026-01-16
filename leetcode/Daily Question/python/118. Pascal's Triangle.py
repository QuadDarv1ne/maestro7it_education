class Solution:
    def generate(self, numRows):
        """
        Генерирует треугольник Паскаля заданной высоты
        
        @param numRows Количество строк в треугольнике
        @return Двумерный список, представляющий треугольник Паскаля
        
        Сложность: O(n²), где n = numRows
        
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
        triangle = []
        
        for row_num in range(numRows):
            row = [1] * (row_num + 1)
            
            for j in range(1, row_num):
                row[j] = triangle[row_num - 1][j - 1] + triangle[row_num - 1][j]
            
            triangle.append(row)
        
        return triangle