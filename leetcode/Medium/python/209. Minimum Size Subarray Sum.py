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
    def minSubArrayLen(self, target, nums):
        """
        Находит минимальную длину подмассива, сумма которого больше или равна target.
        
        Args:
            target (int): Целевая сумма
            nums (List[int]): Массив положительных целых чисел
            
        Returns:
            int: Минимальная длина подмассива с суммой ≥ target. 
                 Если такого подмассива нет, возвращает 0.
                 
        Алгоритм:
            Используется метод скользящего окна с двумя указателями.
            1. Правый указатель расширяет окно, добавляя элементы к текущей сумме.
            2. Когда сумма становится ≥ target, левый указатель сжимает окно,
               пытаясь найти минимальную длину.
            3. Минимальная длина постоянно обновляется.
            
        Сложность:
            Время: O(n) - каждый элемент обрабатывается максимум дважды
            Память: O(1) - константная дополнительная память
            
        Примеры:
            >>> solution = Solution()
            >>> solution.minSubArrayLen(7, [2,3,1,2,4,3])
            2
            >>> solution.minSubArrayLen(4, [1,4,4])
            1
            >>> solution.minSubArrayLen(11, [1,1,1,1,1,1,1,1])
            0
        """
        n = len(nums)
        min_length = float('inf')  # Изначально бесконечность
        current_sum = 0
        left = 0
        
        for right in range(n):
            # Расширяем окно, добавляя элемент справа
            current_sum += nums[right]
            
            # Сжимаем окно, пока сумма >= target
            while current_sum >= target:
                # Обновляем минимальную длину
                min_length = min(min_length, right - left + 1)
                
                # Убираем левый элемент и сдвигаем левый указатель
                current_sum -= nums[left]
                left += 1
        
        # Возвращаем 0, если подмассив не найден
        return min_length if min_length != float('inf') else 0


# Альтернативное решение с предварительным вычислением префиксных сумм и бинарным поиском
class Solution2:
    def minSubArrayLen(self, target, nums):
        """
        Альтернативное решение с использованием префиксных сумм и бинарного поиска.
        Подходит, если массив очень большой и требуется оптимизация.
        """
        n = len(nums)
        min_length = float('inf')
        
        # Создаем массив префиксных сумм
        prefix_sum = [0] * (n + 1)
        for i in range(n):
            prefix_sum[i + 1] = prefix_sum[i] + nums[i]
        
        # Для каждой позиции ищем минимальный подмассив с суммой >= target
        for i in range(n + 1):
            # Ищем минимальный j такой, что prefix_sum[j] - prefix_sum[i] >= target
            # Это эквивалентно поиску prefix_sum[j] >= prefix_sum[i] + target
            to_find = prefix_sum[i] + target
            
            # Бинарный поиск в массиве префиксных сумм
            left, right = i, n
            while left <= right:
                mid = left + (right - left) // 2
                if prefix_sum[mid] >= to_find:
                    min_length = min(min_length, mid - i)
                    right = mid - 1
                else:
                    left = mid + 1
        
        return min_length if min_length != float('inf') else 0