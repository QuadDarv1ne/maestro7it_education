'''
https://leetcode.com/problems/sliding-window-maximum/description/
'''

from collections import deque

class Solution:
    def maxSlidingWindow(self, nums, k):
        """
        Возвращает список максимумов для каждого окна размера k.
        Используется deque для хранения индексов в порядке убывания значений.
        """
        q = deque()     # хранит индексы
        ans = []
        for i, x in enumerate(nums):
            # Удаляем устаревшие индексы (вне окна)
            if q and q[0] < i - k + 1:
                q.popleft()
            # Удаляем все индексы с меньшими значениями
            while q and nums[q[-1]] <= x:
                q.pop()
            q.append(i)
            # Если окно сформировано, добавляем максимум
            if i >= k - 1:
                ans.append(nums[q[0]])
        return ans

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks