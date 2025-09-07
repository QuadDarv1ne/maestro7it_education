'''
https://leetcode.com/contest/weekly-contest-466/problems/count-bowl-subarrays/description/
'''

class Solution:
    def bowlSubarrays(self, nums: List[int]) -> int:
        n,s=len(nums),[]
        c=0
        for x in nums:
            while s and s[-1] < x:
                s.pop()
                c+=1
            if s:  c+=1
            s.append(x)
        return c-(n-1)

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks