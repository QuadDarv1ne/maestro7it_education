'''
https://leetcode.com/problems/longest-subarray-of-1s-after-deleting-one-element/description/?envType=daily-question&envId=2025-08-24
'''

# from typing import List

class Solution:
    # def longestSubarray(self, nums: List[int]) -> int:
    def longestSubarray(self, nums):
        """
        Задача: Найти длину самой длинной подстроки из 1,
        если разрешено удалить ровно один элемент массива.

        Метод:
        - Используем скользящее окно (два указателя).
        - В окне допускаем максимум один ноль.
        - Двигаем правый указатель вправо, считаем количество нулей.
        - Если нулей больше 1 → сдвигаем левый указатель.
        - Ответ = максимальная длина окна - 1 (так как один элемент удаляется).

        Сложность:
        - Время: O(n)
        - Память: O(1)
        """
        ans = 0
        zeros = 0
        left = 0
        for right, x in enumerate(nums):
            if x == 0:
                zeros += 1
            while zeros > 1:
                if nums[left] == 0:
                    zeros -= 1
                left += 1
            ans = max(ans, right - left)
        return ans

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks