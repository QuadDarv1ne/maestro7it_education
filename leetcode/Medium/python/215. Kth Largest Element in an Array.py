'''
https://leetcode.com/problems/kth-largest-element-in-an-array/description/
'''

class Solution:
    def findKthLargest(self, nums, k):
        """
        Находит k-й по величине элемент в массиве nums с помощью min-heap.
        Алгоритм:
        1. Создаем min-heap размером k из первых k элементов.
        2. Для оставшихся элементов массива:
           - если элемент больше корня кучи, заменяем корень на этот элемент.
        3. В конце корень кучи — k-й по величине элемент.

        Время: O(n log k), память: O(k)
        """
        # Создаем кучу из первых k элементов
        heap = nums[:k]
        heapq.heapify(heap)

        # Проходим оставшиеся элементы
        for num in nums[k:]:
            if num > heap[0]:
                heapq.heappushpop(heap, num)

        # Корень кучи — k-й по величине элемент
        return heap[0]

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks