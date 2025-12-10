'''
LeetCode 78: Subsets (Подмножества)
https://leetcode.com/problems/subsets/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Описание задачи:
Дан массив уникальных целых чисел nums. Вернуть все возможные подмножества
(множество степени / power set). Решение не должно содержать дубликаты.

Примеры:
Input: nums = [1,2,3]
Output: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]

Input: nums = [0]
Output: [[],[0]]

Ограничения:
- 1 <= nums.length <= 10
- -10 <= nums[i] <= 10
- Все числа в nums уникальны

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. YouTube канал: https://www.youtube.com/@it-coders
6. ВК группа: https://vk.com/science_geeks
'''

# ========================== PYTHON ==========================

class Solution:
    # ========== ПОДХОД 1: Backtracking (Рекомендуется) ==========
    def subsets(self, nums):
        """
        Генерирует все подмножества используя backtracking.
        
        Идея: Для каждого элемента есть 2 выбора - включить или не включить.
        Это создает дерево решений с 2^n листьями (подмножествами).
        
        Time Complexity: O(n * 2^n)
        - 2^n подмножеств
        - n времени на копирование каждого подмножества
        
        Space Complexity: O(n)
        - Глубина рекурсии = n
        - Не считая результат
        
        Args:
            nums: массив уникальных целых чисел
            
        Returns:
            список всех возможных подмножеств
        """
        result = []
        
        def backtrack(index, path):
            # Каждый путь - это валидное подмножество
            result.append(path[:])  # Копируем текущий путь
            
            # Пробуем добавить оставшиеся элементы
            for i in range(index, len(nums)):
                # Выбираем nums[i]
                path.append(nums[i])
                
                # Рекурсивно строим подмножества, начиная с i+1
                backtrack(i + 1, path)
                
                # Откатываем выбор (backtracking)
                path.pop()
        
        backtrack(0, [])
        return result
    
    # ========== ПОДХОД 2: Итеративный (Каскадный) ==========
    def subsets_iterative(self, nums):
        """
        Генерирует подмножества итеративно.
        
        Идея: Начинаем с [[]], затем для каждого числа добавляем его
        ко всем существующим подмножествам.
        
        Time Complexity: O(n * 2^n)
        Space Complexity: O(1) не считая результат
        """
        result = [[]]  # Начинаем с пустого подмножества
        
        for num in nums:
            # Для каждого числа создаем новые подмножества
            # добавляя его ко всем существующим
            new_subsets = []
            for subset in result:
                new_subsets.append(subset + [num])
            
            # Добавляем новые подмножества к результату
            result.extend(new_subsets)
        
        return result
    
    # ========== ПОДХОД 3: Битовые маски ==========
    def subsets_bitmask(self, nums):
        """
        Генерирует подмножества используя битовые маски.
        
        Идея: Каждое подмножество можно представить битовой маской.
        Например, для [1,2,3]:
        - 000 (0) = []
        - 001 (1) = [3]
        - 010 (2) = [2]
        - 011 (3) = [2,3]
        - 100 (4) = [1]
        - 101 (5) = [1,3]
        - 110 (6) = [1,2]
        - 111 (7) = [1,2,3]
        
        Time Complexity: O(n * 2^n)
        Space Complexity: O(1) не считая результат
        """
        n = len(nums)
        result = []
        
        # Перебираем все числа от 0 до 2^n - 1
        for mask in range(1 << n):  # 1 << n = 2^n
            subset = []
            
            # Проверяем каждый бит маски
            for i in range(n):
                # Если i-й бит установлен, включаем nums[i]
                if mask & (1 << i):
                    subset.append(nums[i])
            
            result.append(subset)
        
        return result