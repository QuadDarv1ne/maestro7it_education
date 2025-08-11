'''
https://leetcode.com/problems/insert-delete-getrandom-o1/description/?envType=study-plan-v2&envId=top-interview-150
'''

import random

class RandomizedSet:
    def __init__(self):
        self.list = []
        self.map = {}

    def insert(self, val):
        if val in self.map:
            return False
        self.map[val] = len(self.list)
        self.list.append(val)
        return True

    def remove(self, val):
        if val not in self.map:
            return False
        index = self.map[val]
        last_element = self.list[-1]
        self.list[index] = last_element
        self.map[last_element] = index
        self.list.pop()
        del self.map[val]
        return True

    def getRandom(self):
        return random.choice(self.list)

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks