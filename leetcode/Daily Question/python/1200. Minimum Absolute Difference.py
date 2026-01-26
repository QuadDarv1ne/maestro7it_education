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
    def minimumAbsDifference(self, arr):
        """
        Находит все пары элементов с минимальной абсолютной разностью в массиве.
        
        Параметры:
            arr: список различных целых чисел.
            
        Возвращает:
            Список пар [a, b], где:
            - a < b
            - |a - b| минимально среди всех возможных пар
            - Пары отсортированы в порядке возрастания внутри каждой пары
              и по первому элементу между парами
            
        Примеры:
            >>> solution = Solution()
            >>> solution.minimumAbsDifference([4,2,1,3])
            [[1,2],[2,3],[3,4]]
            
            >>> solution.minimumAbsDifference([1,3,6,10,15])
            [[1,3]]
        """
        # Сортируем массив для нахождения последовательных элементов с минимальной разностью
        arr.sort()
        
        # Инициализируем минимальную разность бесконечностью
        min_diff = float('inf')
        result = []
        
        # Проходим по отсортированному массиву
        for i in range(1, len(arr)):
            diff = arr[i] - arr[i-1]  # Разность между текущим и предыдущим
            
            if diff < min_diff:
                # Нашли новую минимальную разность - обновляем результат
                min_diff = diff
                result = [[arr[i-1], arr[i]]]
            elif diff == min_diff:
                # Добавляем пару с такой же минимальной разностью
                result.append([arr[i-1], arr[i]])
        
        return result