'''
https://leetcode.com/problems/first-missing-positive/description/
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "First Missing Positive"

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
'''

class Solution(object):
    def firstMissingPositive(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        n = len(nums)
        
        # Первый проход: размещаем числа на своих позициях
        for i in range(n):
            # Пока текущее число в допустимом диапазоне и не на своем месте
            while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
                # Меняем местами текущее число и число на его правильной позиции
                correct_pos = nums[i] - 1
                nums[i], nums[correct_pos] = nums[correct_pos], nums[i]
        
        # Второй проход: ищем первое число, которое не на своем месте
        for i in range(n):
            if nums[i] != i + 1:
                return i + 1
        
        # Если все числа от 1 до n присутствуют, возвращаем n + 1
        return n + 1