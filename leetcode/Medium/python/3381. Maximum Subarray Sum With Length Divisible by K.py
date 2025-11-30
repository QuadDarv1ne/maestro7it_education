"""
https://leetcode.com/problems/maximum-subarray-sum-with-length-divisible-by-k/description/?envType=daily-question&envId=2025-11-27
Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
"""

class Solution:
    def maxSubarraySum(self, nums, k):
        n = len(nums)
        prefix = [0] * (n + 1)
        
        for i in range(n):
            prefix[i + 1] = prefix[i] + nums[i]
        
        max_sum = float('-inf')
        min_prefix = {0: 0}
        
        for i in range(1, n + 1):
            remainder = i % k
            
            if remainder in min_prefix:
                current_sum = prefix[i] - min_prefix[remainder]
                max_sum = max(max_sum, current_sum)
            
            if remainder not in min_prefix:
                min_prefix[remainder] = prefix[i]
            else:
                min_prefix[remainder] = min(min_prefix[remainder], prefix[i])
        
        return max_sum if max_sum != float('-inf') else 0

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks