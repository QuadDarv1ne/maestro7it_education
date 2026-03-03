'''
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
'''

import random

class RandomizedSet:
    def __init__(self):
        self.values = []
        self.index_map = {}

    def insert(self, val):
        if val in self.index_map:
            return False
        self.index_map[val] = len(self.values)
        self.values.append(val)
        return True

    def remove(self, val):
        if val not in self.index_map:
            return False
        # Move the last element to the position of the element to delete
        last_val = self.values[-1]
        idx = self.index_map[val]
        self.values[idx] = last_val
        self.index_map[last_val] = idx
        # Remove the last element
        self.values.pop()
        del self.index_map[val]
        return True

    def getRandom(self):
        return random.choice(self.values)