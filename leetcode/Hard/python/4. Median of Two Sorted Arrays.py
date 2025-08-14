'''
https://leetcode.com/problems/median-of-two-sorted-arrays/description/
'''

class Solution:
    def findMedianSortedArrays(self, nums1, nums2):
        """
        Находит медиану двух отсортированных списков за O(log(min(m,n))) времени.

        Идея:
        - Используем бинарный поиск по меньшему из массивов.
        - Разбиваем объединённые массивы на левую и правую части.
        - Проверяем подходящее разделение по крайним элементам.
        - Вычисляем медиану из max левой части и min правой, в зависимости от чётности.
        """
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1
        m, n = len(nums1), len(nums2)
        left, right = 0, m

        while left <= right:
            i = (left + right) // 2
            j = (m + n + 1) // 2 - i

            maxLeft1 = nums1[i - 1] if i != 0 else float('-inf')
            minRight1 = nums1[i] if i != m else float('inf')
            maxLeft2 = nums2[j - 1] if j != 0 else float('-inf')
            minRight2 = nums2[j] if j != n else float('inf')

            if maxLeft1 <= minRight2 and maxLeft2 <= minRight1:
                if (m + n) % 2 == 0:
                    return (max(maxLeft1, maxLeft2) + min(minRight1, minRight2)) / 2.0
                return max(maxLeft1, maxLeft2)
            elif maxLeft1 > minRight2:
                right = i - 1
            else:
                left = i + 1

        raise ValueError("Input arrays are invalid.")

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks