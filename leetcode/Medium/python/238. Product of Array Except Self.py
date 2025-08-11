'''
https://leetcode.com/problems/product-of-array-except-self/description/?envType=study-plan-v2&envId=top-interview-150
'''

class Solution:
    def productExceptSelf(self, nums):
        """
        Возвращает массив answer, где answer[i] — произведение всех элементов nums,
        кроме nums[i], без использования операции деления.

        Подход: два прохода
        1. Первый проход (слева направо): answer[i] = произведение элементов слева от i
        2. Второй проход (справа налево): умножаем answer[i] на произведение элементов справа от i
        """
        n = len(nums)
        answer = [1] * n

        # Префиксный проход (левые произведения)
        left = 1
        for i in range(n):
            answer[i] = left
            left *= nums[i]

        # Суффиксный проход (правые произведения)
        right = 1
        for i in range(n - 1, -1, -1):
            answer[i] *= right
            right *= nums[i]

        return answer

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks