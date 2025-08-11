'''
https://leetcode.com/problems/trapping-rain-water/description/?envType=study-plan-v2&envId=top-interview-150
'''

class Solution:
    def trap(self, height):
        """
        Вычисляет объем воды, который можно собрать после дождя между столбцами.

        Алгоритм:
        1. Два указателя: left (слева), right (справа).
        2. left_max — максимальная высота слева, right_max — справа.
        3. Если height[left] < height[right]:
            - Если height[left] >= left_max → обновляем left_max.
            - Иначе добавляем (left_max - height[left]) в результат.
        4. Аналогично для правого указателя.

        :param height: Список целых чисел — высоты столбцов.
        :return: Целое число — общий объем воды.
        
        Сложность:
        - Время: O(n)
        - Память: O(1)
        """
        left, right = 0, len(height) - 1
        left_max, right_max = 0, 0
        water = 0

        while left < right:
            if height[left] < height[right]:
                if height[left] >= left_max:
                    left_max = height[left]
                else:
                    water += left_max - height[left]
                left += 1
            else:
                if height[right] >= right_max:
                    right_max = height[right]
                else:
                    water += right_max - height[right]
                right -= 1

        return water

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks