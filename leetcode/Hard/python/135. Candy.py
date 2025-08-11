'''
https://leetcode.com/problems/candy/description/?envType=study-plan-v2&envId=top-interview-150
'''

class Solution:
    def candy(self, ratings):
        """
        Определяет минимальное количество конфет для детей с рейтингами ratings.

        Параметры:
        ----------
        ratings : List[int]
            Список рейтингов детей.

        Возвращает:
        -----------
        int
            Минимальное количество конфет, чтобы удовлетворить условия.

        Алгоритм:
        ---------
        1. Инициализируем список candies с 1 конфетой каждому ребенку.
        2. Проходим слева направо: если rating[i] > rating[i-1], candies[i] = candies[i-1] + 1.
        3. Проходим справа налево: если rating[i] > rating[i+1], candies[i] = max(candies[i], candies[i+1] + 1).
        4. Суммируем candies и возвращаем результат.
        """
        n = len(ratings)
        candies = [1] * n

        for i in range(1, n):
            if ratings[i] > ratings[i - 1]:
                candies[i] = candies[i - 1] + 1

        for i in range(n - 2, -1, -1):
            if ratings[i] > ratings[i + 1]:
                candies[i] = max(candies[i], candies[i + 1] + 1)

        return sum(candies)

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks