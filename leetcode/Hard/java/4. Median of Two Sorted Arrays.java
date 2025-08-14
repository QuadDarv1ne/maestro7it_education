/**
 * https://leetcode.com/problems/median-of-two-sorted-arrays/description/
 */

/**
 * Решение задачи медианы двух отсортированных массивов с бинарным поиском.
 *
 * @param nums1 первый массив
 * @param nums2 второй массив
 * @return медиана как double
 */
class Solution {
    public double findMedianSortedArrays(int[] nums1, int[] nums2) {
        if (nums1.length > nums2.length) return findMedianSortedArrays(nums2, nums1);
        int n1 = nums1.length, n2 = nums2.length;
        int left = 0, right = n1;
        while (left <= right) {
            int part1 = (left + right) / 2;
            int part2 = (n1 + n2 + 1) / 2 - part1;

            int maxLeft1 = part1 == 0 ? Integer.MIN_VALUE : nums1[part1 - 1];
            int minRight1 = part1 == n1 ? Integer.MAX_VALUE : nums1[part1];
            int maxLeft2 = part2 == 0 ? Integer.MIN_VALUE : nums2[part2 - 1];
            int minRight2 = part2 == n2 ? Integer.MAX_VALUE : nums2[part2];

            if (maxLeft1 <= minRight2 && maxLeft2 <= minRight1) {
                if ((n1 + n2) % 2 == 0) {
                    return (Math.max(maxLeft1, maxLeft2) + Math.min(minRight1, minRight2)) / 2.0;
                } else {
                    return Math.max(maxLeft1, maxLeft2);
                }
            } else if (maxLeft1 > minRight2) {
                right = part1 - 1;
            } else {
                left = part1 + 1;
            }
        }
        throw new IllegalArgumentException();
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