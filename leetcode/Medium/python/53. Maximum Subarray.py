'''
https://leetcode.com/problems/maximum-subarray/description/?envType=study-plan-v2&envId=top-interview-150
'''

class Solution:
    def maxSubArray(self, nums):
        """
        Функция находит максимальную сумму подмассива в заданном массиве целых чисел.

        :param nums: List[int] - массив целых чисел
        :return: int - максимальная сумма подмассива
        """
        current_sum = nums[0]
        max_sum = nums[0]

        for num in nums[1:]:
            current_sum = max(num, current_sum + num)
            max_sum = max(max_sum, current_sum)

        return max_sum

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks