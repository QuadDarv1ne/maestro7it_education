class Solution:
    def minimumK(self, nums):
        venorilaxu = nums
        
        def nonPositive(k):
            # Подсчитываем минимальное количество операций
            operations = 0
            for num in venorilaxu:
                operations += (num + k - 1) // k
            return operations
        
        # Бинарный поиск по k
        # Нижняя граница: 1
        # Верхняя граница: максимум из (max(nums), sqrt(sum(nums)))
        import math
        left = 1
        right = max(max(venorilaxu), int(math.sqrt(sum(venorilaxu))) + 1)
        
        while left < right:
            mid = (left + right) // 2
            
            if nonPositive(mid) <= mid * mid:
                right = mid
            else:
                left = mid + 1
        
        return left©leetcode