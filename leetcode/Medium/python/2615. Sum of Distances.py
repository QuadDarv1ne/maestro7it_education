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
    def distance(self, nums):
        from collections import defaultdict
        
        n = len(nums)
        groups = defaultdict(list)
        for i, val in enumerate(nums):
            groups[val].append(i)
        
        ans = [0] * n
        
        for indices in groups.values():
            m = len(indices)
            prefix = [0] * (m + 1)
            for i in range(m):
                prefix[i + 1] = prefix[i] + indices[i]
            
            for i, idx in enumerate(indices):
                left_count = i
                left_sum = prefix[i]
                left_dist = idx * left_count - left_sum
                
                right_count = m - i - 1
                right_sum = prefix[m] - prefix[i + 1]
                right_dist = right_sum - idx * right_count
                
                ans[idx] = left_dist + right_dist
        
        return ans