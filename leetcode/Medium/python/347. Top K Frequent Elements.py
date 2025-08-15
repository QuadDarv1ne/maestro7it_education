'''
https://leetcode.com/problems/top-k-frequent-elements/
'''

from collections import Counter

class Solution:
    def topKFrequent(self, nums, k):
        # 1. Подсчёт частот
        count = Counter(nums)
        # 2. Корзины по частотам
        buckets = [[] for _ in range(len(nums) + 1)]
        for num, freq in count.items():
            buckets[freq].append(num)
        # 3. Сбор результатов с конца
        res = []
        for freq in range(len(buckets) - 1, -1, -1):
            for num in buckets[freq]:
                res.append(num)
                if len(res) == k:
                    return res

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks