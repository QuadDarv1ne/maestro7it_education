'''
https://leetcode.com/problems/find-the-number-of-ways-to-place-people-ii/description/?envType=daily-question&envId=2025-09-03
'''

class Solution:
    def numberOfPairs(self, points):
        """
        Возвращает количество допустимых пар (Alice, Bob), таких что
        Alice является верхним левым углом, Bob — нижним правым, и
        внутри или на границе прямоугольника нет других точек.
        """
        # Сортировка: по x по возрастанию, при равных x — y по убыванию
        points.sort(key=lambda p: (p[0], -p[1]))
        ans = 0
        n = len(points)
        for i in range(n):
            max_y = float('-inf')
            y1 = points[i][1]
            for j in range(i + 1, n):
                y2 = points[j][1]
                # Условие: y2 ≤ y1 и больше предыдущего max_y
                if max_y < y2 <= y1:
                    ans += 1
                    max_y = y2
        return ans

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks