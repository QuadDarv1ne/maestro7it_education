'''
https://leetcode.com/problems/avoid-flood-in-the-city/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

from sortedcontainers import SortedList

class Solution(object):
    def avoidFlood(self, rains):
        """
        Решение задачи "Avoid Flood in The City" (LeetCode 1488).

        Идея:
        - Используем словарь lastRain для хранения последнего дня дождя над озером.
        - Список dryDays хранит индексы сухих дней (SortedList для поиска первого дня > lastRain[lake]).
        - Когда дождь идёт над озером, которое уже полное:
            • Ищем ближайший сухой день после предыдущего дождя над этим озером.
            • Если такой день найден — осушаем озеро в этот день.
            • Если нет — наводнение (return []).
        - День сухой (0) добавляем в dryDays и позднее используем для осушения.
        """
        from collections import defaultdict
        lastRain = {}
        dryDays = SortedList()
        res = [-1]*len(rains)

        for i, lake in enumerate(rains):
            if lake == 0:
                dryDays.add(i)
                res[i] = 1  # по умолчанию осушаем любое озеро
            else:
                if lake in lastRain:
                    idx = dryDays.bisect_right(lastRain[lake])
                    if idx == len(dryDays):
                        return []  # нет сухого дня → наводнение
                    dry_idx = dryDays[idx]
                    res[dry_idx] = lake  # осушаем именно это озеро
                    dryDays.pop(idx)
                lastRain[lake] = i
                res[i] = -1  # дождь над озером
        return res

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks