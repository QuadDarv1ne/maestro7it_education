'''
https://leetcode.com/problems/find-the-number-of-ways-to-place-people-i/description/?envType=daily-question&envId=2025-09-02
'''

class Solution:
    def numberOfPairs(self, points):
        """
        Задача:
        Найти количество способов выбрать упорядоченные пары точек (i, j),
        такие что:
        1) x1 <= x2 и y1 >= y2
        2) в прямоугольнике, образованном (x1, y1) и (x2, y2), нет других точек

        :param points: список точек [x, y]
        :return: количество допустимых пар (int)
        """
        n = len(points)
        ans = 0

        for i in range(n):
            x1, y1 = points[i]
            for j in range(n):
                if i == j:
                    continue
                x2, y2 = points[j]
                if x1 <= x2 and y1 >= y2:
                    blocked = False
                    for k in range(n):
                        if k == i or k == j:
                            continue
                        xk, yk = points[k]
                        if x1 <= xk <= x2 and y2 <= yk <= y1:
                            blocked = True
                            break
                    if not blocked:
                        ans += 1

        return ans

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks