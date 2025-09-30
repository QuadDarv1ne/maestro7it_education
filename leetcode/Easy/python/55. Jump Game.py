'''
https://leetcode.com/problems/jump-game/description/?envType=study-plan-v2&envId=top-interview-150

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

class Solution:
    def canJump(self, nums):
        """
        :param nums: Список неотрицательных целых — максимальные прыжки
        :return: True, если можно добраться до последнего индекса, иначе False

        Алгоритм:
        - Идём по массиву, поддерживая maxReach — максимально достижимый индекс
        - Если текущий индекс i больше maxReach, значит сюда не добраться — возвращаем False
        - Обновляем maxReach = max(maxReach, i + nums[i])
        - Если maxReach ≥ последний индекс, возвращаем True
        Сложность: O(n) времени, O(1) памяти
        """
        maxReach = 0
        last = len(nums) - 1
        for i, jump in enumerate(nums):
            if i > maxReach:
                return False
            maxReach = max(maxReach, i + jump)
            if maxReach >= last:
                return True
        return False


''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks