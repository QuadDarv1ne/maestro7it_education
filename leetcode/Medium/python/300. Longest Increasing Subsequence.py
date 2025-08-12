'''
https://leetcode.com/problems/longest-increasing-subsequence/description/?envType=study-plan-v2&envId=top-interview-150
'''

from bisect import bisect_left

class Solution:
    def lengthOfLIS(self, nums):
        """
        Находит длину самой длинной строго возрастающей подпоследовательности в списке nums.
        Использует двоичный поиск для эффективного решения задачи за O(n log n).
        
        :param nums: Список целых чисел.
        :return: Длина самой длинной возрастающей подпоследовательности.
        """
        tails = []
        for num in nums:
            # Находим индекс, куда можно вставить num, чтобы сохранить отсортированность
            idx = bisect_left(tails, num)
            if idx == len(tails):
                tails.append(num)
            else:
                tails[idx] = num
        return len(tails)

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks