'''
Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. YouTube канал: https://www.youtube.com/@it-coders
6. ВК группа: https://vk.com/science_geeks
'''

class Solution:
    def findMin(self, nums):
        """
        Находит минимальный элемент в повернутом отсортированном массиве.
        
        Параметры:
        nums - список уникальных целых чисел, отсортированный по возрастанию и повернутый
        
        Возвращает:
        Минимальный элемент массива
        
        Алгоритм:
        - Используем бинарный поиск
        - Сравниваем средний элемент с крайним правым
        - Если nums[mid] > nums[right], значит минимум в правой половине
        - Иначе минимум в левой половине (включая mid)
        """
        left, right = 0, len(nums) - 1
        
        # Массив не повернут или содержит 1 элемент
        if nums[left] < nums[right] or left == right:
            return nums[left]
        
        while left < right:
            mid = left + (right - left) // 2
            
            # Сравниваем с крайним правым элементом
            if nums[mid] > nums[right]:
                # Минимум в правой половине (после mid)
                left = mid + 1
            else:
                # Минимум в левой половине (может быть mid)
                right = mid
        
        return nums[left]