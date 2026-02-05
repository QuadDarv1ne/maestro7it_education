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
    def constructTransformedArray(self, nums):
        """
        Создает трансформированный массив на основе циклического массива nums.
        
        Для каждого индекса i:
        - Если nums[i] > 0: перемещаемся на nums[i] шагов вправо (с зацикливанием)
        - Если nums[i] < 0: перемещаемся на |nums[i]| шагов влево (с зацикливанием)
        - Если nums[i] == 0: result[i] = 0
        
        Аргументы:
            nums: List[int] - входной массив целых чисел
            
        Возвращает:
            List[int] - трансформированный массив той же длины
            
        Временная сложность: O(n)
        Пространственная сложность: O(n)
        """
        n = len(nums)
        result = [0] * n  # Инициализируем результирующий массив нулями
        
        for i in range(n):
            # Вычисляем целевой индекс с учетом зацикливания
            # Формула (i + nums[i]) % n работает для всех случаев:
            # - nums[i] > 0: движение вправо
            # - nums[i] < 0: движение влево (Python корректно обрабатывает отрицательный модуло)
            # - nums[i] == 0: остаемся на месте, result[i] = nums[i] = 0
            target_index = (i + nums[i]) % n
            result[i] = nums[target_index]
        
        return result
