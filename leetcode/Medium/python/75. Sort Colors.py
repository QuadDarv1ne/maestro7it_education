class Solution:
    def sortColors(self, nums: list[int]) -> None:
        """
        Сортировка цветов (Dutch National Flag алгоритм)
        
        Алгоритм: Three-way partition (трёхчастное разбиение)
        Сложность: O(n) по времени, O(1) по памяти
        Проходим массив один раз
        
        Args:
            nums: список целых чисел (0, 1, 2)
            
        Returns:
            None: сортирует массив на месте
        """
        # Указатели для трех частей:
        # low - конец нулей, mid - текущий элемент, high - начало двоек
        low, mid, high = 0, 0, len(nums) - 1
        
        while mid <= high:
            if nums[mid] == 0:
                # Обмен и сдвиг указателей для нулей
                nums[low], nums[mid] = nums[mid], nums[low]
                low += 1
                mid += 1
            elif nums[mid] == 1:
                # Единицы остаются на месте, просто двигаем mid
                mid += 1
            else:  # nums[mid] == 2
                # Обмен и сдвиг указателя для двоек
                nums[mid], nums[high] = nums[high], nums[mid]
                high -= 1
                # Не увеличиваем mid, так как нужно проверить новый элемент
    
    def sortColors_counting(self, nums: list[int]) -> None:
        """
        Альтернативное решение: counting sort (подсчет)
        Сложность: O(n) по времени, O(1) по памяти (поскольку только 3 цвета)
        """
        count_0 = count_1 = count_2 = 0
        
        # Подсчитываем количество каждого цвета
        for num in nums:
            if num == 0:
                count_0 += 1
            elif num == 1:
                count_1 += 1
            else:
                count_2 += 1
        
        # Заполняем массив в правильном порядке
        nums[:count_0] = [0] * count_0
        nums[count_0:count_0 + count_1] = [1] * count_1
        nums[count_0 + count_1:] = [2] * count_2


# Тестирование
def test_sort_colors():
    solution = Solution()
    
    test_cases = [
        ([2,0,2,1,1,0], [0,0,1,1,2,2]),
        ([2,0,1], [0,1,2]),
        ([0], [0]),
        ([1,0], [0,1]),
        ([2,2,2,2], [2,2,2,2]),
        ([1,1,1,1], [1,1,1,1]),
        ([0,0,0,0], [0,0,0,0]),
        ([2,1,0], [0,1,2]),
    ]
    
    for nums, expected in test_cases:
        nums_copy = nums.copy()
        solution.sortColors(nums_copy)
        assert nums_copy == expected, f"Failed: {nums} -> {nums_copy}, expected {expected}"
        print(f"✓ {nums} -> {nums_copy}")
    
    print("\nВсе тесты пройдены успешно!")


if __name__ == "__main__":
    test_sort_colors()