'''
https://leetcode.com/problems/maximum-sum-circular-subarray/description/?envType=study-plan-v2&envId=top-interview-150
'''

class Solution:
    def maxSubarraySumCircular(self, nums):
        def kadane(arr):
            max_sum = curr_sum = arr[0]
            for num in arr[1:]:
                curr_sum = max(num, curr_sum + num)
                max_sum = max(max_sum, curr_sum)
            return max_sum

        total_sum = sum(nums)
        max_sum = kadane(nums)
        min_sum = kadane([-num for num in nums])
        
        # если все числа отрицательные, возвращаем max_sum
        if total_sum == -min_sum:
            return max_sum
        
        return max(max_sum, total_sum + min_sum)

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks