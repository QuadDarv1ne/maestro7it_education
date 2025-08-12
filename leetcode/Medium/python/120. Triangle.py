'''
https://leetcode.com/problems/triangle/description/?envType=study-plan-v2&envId=top-interview-150
'''

class Solution:
    def minimumTotal(self, triangle):
        """
        Находит минимальную сумму пути от вершины треугольника до основания.
        Двигаемся по соседним числам на каждом уровне, используя динамическое программирование.
        
        :param triangle: Список списков, представляющий треугольник чисел.
        :return: Минимальная сумма пути.
        """
        dp = triangle[-1][:]  # Копируем последний уровень треугольника с помощью среза
        
        for row in range(len(triangle) - 2, -1, -1):
            for i in range(len(triangle[row])):
                dp[i] = triangle[row][i] + min(dp[i], dp[i + 1])
        
        return dp[0]

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks