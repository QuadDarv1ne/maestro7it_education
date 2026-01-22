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

# from typing import List

class Solution:
    def minimumPairRemoval(self, nums):
        """
        Возвращает минимальное количество операций для сортировки массива.
        
        Операция: выбрать соседнюю пару с минимальной суммой (самую левую при равенстве),
        заменить пару на их сумму.
        """
        # Создаем копию массива для модификации
        arr = nums[:]
        operations = 0
        
        # Проверка, является ли массив неубывающим
        def is_non_decreasing(a):
            for i in range(1, len(a)):
                if a[i] < a[i - 1]:
                    return False
            return True
        
        # Пока массив не отсортирован
        while not is_non_decreasing(arr):
            # Находим индекс левого элемента пары с минимальной суммой
            min_sum = arr[0] + arr[1]
            min_index = 0
            
            for i in range(1, len(arr) - 1):
                current_sum = arr[i] + arr[i + 1]
                if current_sum < min_sum:
                    min_sum = current_sum
                    min_index = i
            
            # Заменяем левый элемент на сумму и удаляем правый
            arr[min_index] = min_sum
            arr.pop(min_index + 1)
            operations += 1
        
        return operations