'''
https://leetcode.com/problems/maximum-average-pass-ratio/description/?envType=daily-question&envId=2025-09-01
'''

# Идея: max-куча по приросту. heapq — минимальная куча, поэтому используем отрицательные дельты.
import heapq

class Solution:
    def maxAverageRatio(self, classes, extraStudents):
        def gain(p, t):
            return (p + 1) / (t + 1) - p / t

        # Куча хранит кортежи (-gain, index).
        # Сам список classes будем изменять in-place.
        heap = []
        for i, (p, t) in enumerate(classes):
            heap.append((-gain(p, t), i))
        heapq.heapify(heap)

        for _ in range(extraStudents):
            neg_g, i = heapq.heappop(heap)
            # обновляем сам класс в списке
            classes[i][0] += 1
            classes[i][1] += 1
            # пересчитываем приоритет и возвращаем в кучу
            heapq.heappush(heap, (-gain(classes[i][0], classes[i][1]), i))

        # итог: средняя доля
        total = 0.0
        for p, t in classes:
            total += p / t
        return total / len(classes)

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks