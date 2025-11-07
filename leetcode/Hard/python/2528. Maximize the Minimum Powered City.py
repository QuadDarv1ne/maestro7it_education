'''
https://leetcode.com/problems/maximize-the-minimum-powered-city/description/?envType=daily-question&envId=2025-11-07
Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X  
GitHub: https://github.com/QuadDarv1ne/  
'''

class Solution(object):
    def maxPower(self, stations, r, k):
        n = len(stations)
        
        # Шаг 1: построим начальный массив мощностей через разностный массив
        diff = [0] * (n + 1)
        for i, cnt in enumerate(stations):
            left = max(0, i - r)
            right = min(n - 1, i + r)
            diff[left] += cnt
            diff[right + 1] -= cnt
        
        # Восстанавливаем исходные мощности
        power = [0] * n
        power[0] = diff[0]
        for i in range(1, n):
            power[i] = power[i - 1] + diff[i]
        
        # Вложенная функция с замыканием (имеет доступ к power, n, r, k)
        def can_achieve(target):
            # Копируем текущие мощности логически (без deepcopy — работаем с diff-подходом)
            add_diff = [0] * (n + 1)  # разностный массив для добавленных станций
            curr_add = 0  # текущий вклад добавленных станций в городе i
            used = 0

            for i in range(n):
                curr_add += add_diff[i]
                total = power[i] + curr_add
                if total < target:
                    need = target - total
                    used += need
                    if used > k:
                        return False
                    # Ставим станции в максимально правую позицию, которая ещё покрывает i: j = i + r
                    j = min(i + r, n - 1)
                    curr_add += need
                    # Эффект длится до j + r включительно → снимаем на j + r + 1
                    end = j + r + 1
                    if end < n:
                        add_diff[end] -= need
            return True

        # Бинарный поиск по ответу
        lo = min(power)
        hi = max(power) + k  # теоретический максимум минимума
        ans = lo
        while lo <= hi:
            mid = (lo + hi) // 2
            if can_achieve(mid):
                ans = mid
                lo = mid + 1
            else:
                hi = mid - 1
        return ans

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks