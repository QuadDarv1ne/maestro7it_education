'''
https://leetcode.com/problems/subarray-sum-equals-k/description/
'''

class Solution:
    def subarraySum(self, nums, k):
        """
        Задача: найти количество подмассивов, сумма которых равна k.

        Алгоритм:
        1. Используем префиксные суммы.
        2. Словарь (Counter) хранит количество вхождений каждой суммы.
        3. Для каждой позиции проверяем, встречался ли prefix_sum - k.
        4. Если да — увеличиваем счётчик на количество таких случаев.

        Сложность:
        - Время: O(n), где n — длина массива
        - Память: O(n), для хранения словаря префиксных сумм
        """
        prefix_counts = Counter({0: 1})
        current_sum = 0
        count = 0
        for num in nums:
            current_sum += num
            count += prefix_counts[current_sum - k]
            prefix_counts[current_sum] += 1
        return count

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks