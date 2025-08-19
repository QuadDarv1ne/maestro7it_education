'''
https://leetcode.com/problems/container-with-most-water/description/
'''

class Solution:
    def maxArea(self, height):
        """
        Находит максимальную площадь контейнера для воды.

        Даны n вертикальных линий с высотами height[i]. 
        Нужно выбрать две линии так, чтобы они вместе с осью X образовали контейнер, 
        который вмещает максимальное количество воды.

        Алгоритм:
        - Используется два указателя: left в начале, right в конце массива.
        - На каждом шаге вычисляется площадь: 
            area = (right - left) * min(height[left], height[right]).
        - Указатель с меньшей высотой двигается внутрь, 
          так как именно он ограничивает возможную площадь.
        - Работает за O(n), требует O(1) памяти.

        :param height: список высот вертикальных линий
        :return: максимальная площадь контейнера
        """
        left, right = 0, len(height) - 1
        max_area = 0
        while left < right:
            area = (right - left) * min(height[left], height[right])
            max_area = max(max_area, area)
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
        return max_area

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks