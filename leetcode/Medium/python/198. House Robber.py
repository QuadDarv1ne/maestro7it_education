'''
https://leetcode.com/problems/house-robber/description/?envType=study-plan-v2&envId=top-interview-150
'''

class Solution:
    def rob(self, nums):
        """
        Задача: Максимизировать сумму украденных денег из домов, расположенных в ряд.
        Ограничение: нельзя грабить два соседних дома.

        :param nums: список целых чисел, где nums[i] — количество денег в i-ом доме
        :return: максимальная сумма, которую можно украсть
        """
        n = len(nums)
        if n == 0:
            return 0
        if n == 1:
            return nums[0]

        # dp[i] — максимальная сумма при рассмотрении первых i+1 домов
        dp = [0] * n
        dp[0] = nums[0]
        dp[1] = max(nums[0], nums[1])

        for i in range(2, n):
            # либо не грабим i-й дом, либо грабим и прибавляем dp[i-2]
            dp[i] = max(dp[i-1], dp[i-2] + nums[i])

        return dp[-1]



''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks