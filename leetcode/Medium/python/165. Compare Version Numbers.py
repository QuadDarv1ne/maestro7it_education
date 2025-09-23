'''
https://leetcode.com/problems/compare-version-numbers/description/?envType=daily-question&envId=2025-09-23
'''

class Solution:
    def compareVersion(self, version1, version2):
        """
        Сравнение двух версий version1 и version2.

        Алгоритм:
        1. Разбиваем строки по точке, получаем список частей.
        2. Каждую часть преобразуем в целое число (ведущие нули игнорируются).
        3. Сравниваем части по порядку:
           - если одна версия короче, недостающие части считаем равными 0;
           - если в какой-то позиции v1 < v2 → вернуть -1;
           - если v1 > v2 → вернуть 1.
        4. Если все части равны → вернуть 0.

        :param version1: строка первой версии, например "1.01"
        :param version2: строка второй версии, например "1.001"
        :return: -1 если version1 < version2,
                 1 если version1 > version2,
                 0 если версии равны
        """
        parts1 = version1.split('.')
        parts2 = version2.split('.')
        n1 = len(parts1)
        n2 = len(parts2)
        max_len = max(n1, n2)
        for i in range(max_len):
            v1 = int(parts1[i]) if i < n1 else 0
            v2 = int(parts2[i]) if i < n2 else 0
            if v1 < v2:
                return -1
            elif v1 > v2:
                return 1
        return 0

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks