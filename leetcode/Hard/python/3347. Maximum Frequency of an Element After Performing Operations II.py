'''
Задача: Maximum Frequency of an Element After Performing Operations II  
Источник: https://leetcode.com/problems/maximum-frequency-of-an-element-after-performing-operations-ii/

Описание:
    Дан массив nums длиной n, а также два параметра:
        k — максимально возможное изменение одного элемента за одну операцию (диапазон добавляемого целого: [-k, k]),
        numOperations — количество доступных операций.
    За одну операцию можно выбрать неповторяющийся индекс i и добавить целое в диапазоне [-k, k] к nums[i].
    Нужно вернуть максимальную возможную частоту любого значения в nums после выполнения не более numOperations операций.

Автор: Дуплей Максим Игоревич  
ORCID: https://orcid.org/0009-0007-7605-539X  
GitHub: https://github.com/QuadDarv1ne/  
'''

from collections import Counter
import bisect

class Solution:
    def maxFrequency(self, nums, k, numOperations):
        if not nums:
            return 0

        n = len(nums)
        nums.sort()
        freq = Counter(nums)

        ans = 1

        # 1) Для каждого существующего значения v = nums[i] подсчитать, сколько элементов имеют nums[j] в [v-k, v+k] (бинпоиск).
        #    Достижимая частота для v: min(cover_count, freq[v] + numOperations).
        unique_vals = sorted(freq.keys())
        for v in unique_vals:
            left = bisect.bisect_left(nums, v - k)
            right = bisect.bisect_right(nums, v + k) - 1
            cover = 0
            if right >= left:
                cover = right - left + 1
            candidate = min(cover, freq[v] + numOperations)
            if candidate > ans:
                ans = candidate

        # 2) Но оптимум может достигаться в точке v, которой нет в nums.
        events = []
        for a in nums:
            start = a - k
            end = a + k
            events.append((start, 1))
            # используем end+1 для корректного подсчёта целых точек в закрытом интервале
            events.append((end + 1, -1))
        events.sort()

        cur = 0
        max_cover = 0
        for pos, delta in events:
            cur += delta
            if cur > max_cover:
                max_cover = cur

        # взяли минимум с numOperations (поскольку у нас нет существующих элементов в этом варианте)
        candidate2 = min(max_cover, numOperations)
        if candidate2 > ans:
            ans = candidate2

        return ans


# Примеры и проверка проблемных тестов
if __name__ == "__main__":
    s = Solution()
    # из editorial
    print(s.maxFrequency([42, 11, 52], 96, 1))   # Ожидается: 2
    # проблемный тест, где нужно получить 3
    print(s.maxFrequency([85, 37, 2], 45, 3))    # Ожидается: 3
    # другие примеры
    print(s.maxFrequency([1, 2, 4], 2, 2))       # Ожидается: 3
    print(s.maxFrequency([1, 4, 5], 1, 2))       # Ожидается: 2

'''
Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
8. Официальный сайт школы Maestro7IT: https://school-maestro7it.ru/
'''
