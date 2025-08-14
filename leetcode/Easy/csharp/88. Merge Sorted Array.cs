/**
 * https://leetcode.com/problems/merge-sorted-array/description/
 */

using System;

/**
 * Перемешивает два отсортированных массива в nums1 in-place.
 *
 * nums1 имеет длину m + n. Первые m элементов — значимые, далее место для nums2.
 */
public class Solution {
    public void Merge(int[] nums1, int m, int[] nums2, int n) {
        int write = m + n - 1;
        int i = m - 1;
        int j = n - 1;
        while (j >= 0) {
            if (i >= 0 && nums1[i] > nums2[j]) {
                nums1[write--] = nums1[i--];
            } else {
                nums1[write--] = nums2[j--];
            }
        }
    }
}

/*
''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/