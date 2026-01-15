"""
Максимальная площадь квадратного отверстия в сетке

Сложность: O(h log h + v log v) время, O(1) память
"""
class Solution:
    def maximizeSquareHoleArea(self, n, m, hBars, vBars):
        hBars.sort()
        vBars.sort()
        
        def max_consecutive(arr):
            if not arr:
                return 0
            max_gap = 1
            current = 1
            for i in range(1, len(arr)):
                if arr[i] == arr[i-1] + 1:
                    current += 1
                else:
                    max_gap = max(max_gap, current)
                    current = 1
            return max(max_gap, current)
        
        max_h = max_consecutive(hBars)
        max_v = max_consecutive(vBars)
        
        side = min(max_h, max_v) + 1
        return side * side