'''
https://leetcode.com/problems/design-movie-rental-system/description/?envType=daily-question&envId=2025-09-21
'''

from collections import defaultdict
from bisect import insort, bisect_left

class MovieRentingSystem:
    """
    Реализация системы аренды фильмов.
    """
    def __init__(self, n, entries):
        self.priceMap = {}  # (shop, movie) -> price
        self.available = defaultdict(list)  # movie -> sorted list of (price, shop)
        self.rented = []  # глобальный список арендованных (price, shop, movie)

        for shop, movie, price in entries:
            self.priceMap[(shop, movie)] = price
            insort(self.available[movie], (price, shop))

    def search(self, movie):
        return [shop for price, shop in self.available[movie][:5]]

    def rent(self, shop, movie):
        price = self.priceMap[(shop, movie)]
        arr = self.available[movie]
        i = bisect_left(arr, (price, shop))
        if i < len(arr) and arr[i] == (price, shop):
            arr.pop(i)
        insort(self.rented, (price, shop, movie))

    def drop(self, shop, movie):
        price = self.priceMap[(shop, movie)]
        i = bisect_left(self.rented, (price, shop, movie))
        if i < len(self.rented) and self.rented[i] == (price, shop, movie):
            self.rented.pop(i)
        insort(self.available[movie], (price, shop))

    def report(self):
        return [[shop, movie] for price, shop, movie in self.rented[:5]]

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks