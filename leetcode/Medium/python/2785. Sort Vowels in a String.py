'''
https://leetcode.com/problems/sort-vowels-in-a-string/description/?envType=daily-question&envId=2025-09-11
'''

class Solution:
    def sortVowels(self, s):
        """
        Функция принимает строку и сортирует все гласные буквы
        в порядке возрастания (по Unicode), оставляя согласные и другие символы
        на прежних местах.
        
        Алгоритм:
        1. Собираем все гласные в список.
        2. Сортируем список.
        3. Подставляем обратно на места гласных.
        
        Временная сложность: O(n log n), где n — количество гласных.
        :param s: исходная строка
        :return: новая строка с отсортированными гласными
        """
        def is_vowel(c):
            return c.lower() in {'a','e','i','o','u'}
        
        vowels = [c for c in s if is_vowel(c)]
        vowels.sort()
        vi = 0
        res = []
        for c in s:
            if is_vowel(c):
                res.append(vowels[vi])
                vi += 1
            else:
                res.append(c)
        return ''.join(res)

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks