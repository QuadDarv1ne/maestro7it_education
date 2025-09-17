'''
https://leetcode.com/problems/design-a-food-rating-system/description/?envType=daily-question&envId=2025-09-17
'''

from sortedcontainers import SortedList

class FoodRatings:
    """
    Класс системы рейтингов блюд.

    Атрибуты:
    - food_to_cuisine: dict, food_name -> cuisine
    - food_to_rating: dict, food_name -> current rating
    - cuisine_to_list: dict, cuisine -> SortedList из кортежей (-rating, food_name)

    Методы:
    - __init__: построение структуры
    - changeRating: обновление рейтинга
    - highestRated: возвращение блюда с наивысшим рейтингом для кухни
    """

    def __init__(self, foods, cuisines, ratings):
        self.food_to_cuisine = {}
        self.food_to_rating = {}
        self.cuisine_to_list = {}
        for food, cuisine, rating in zip(foods, cuisines, ratings):
            self.food_to_cuisine[food] = cuisine
            self.food_to_rating[food] = rating
            if cuisine not in self.cuisine_to_list:
                # SortedList, сортируем по ключу: сначала по -rating, потом по food (лексикографически)
                self.cuisine_to_list[cuisine] = SortedList(key=lambda x: (-x[0], x[1]))
            self.cuisine_to_list[cuisine].add((rating, food))

    def changeRating(self, food, newRating):
        cuisine = self.food_to_cuisine[food]
        oldRating = self.food_to_rating[food]
        # удаляем старую пару
        self.cuisine_to_list[cuisine].remove((oldRating, food))
        # добавляем новую
        self.cuisine_to_list[cuisine].add((newRating, food))
        # обновляем хранилища
        self.food_to_rating[food] = newRating

    def highestRated(self, cuisine):
        # первый элемент в SortedList имеет максимальный рейтинг (благодаря ключу)
        rating, food = self.cuisine_to_list[cuisine][0]
        return food

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks