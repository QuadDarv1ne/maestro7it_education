/**
 * https://leetcode.com/problems/median-of-two-sorted-arrays/description/
 */

/// <summary>
/// Вычисляет медиану двух отсортированных массивов за логарифмическое время.
/// </summary>
public class Solution {
    public double FindMedianSortedArrays(int[] nums1, int[] nums2) {
        if (nums1.Length > nums2.Length) return FindMedianSortedArrays(nums2, nums1);
        int n1 = nums1.Length, n2 = nums2.Length;
        int left = 0, right = n1;

        while (left <= right) {
            int part1 = (left + right) / 2;
            int part2 = (n1 + n2 + 1) / 2 - part1;

            int maxLeft1 = part1 == 0 ? int.MinValue : nums1[part1 - 1];
            int minRight1 = part1 == n1 ? int.MaxValue : nums1[part1];
            int maxLeft2 = part2 == 0 ? int.MinValue : nums2[part2 - 1];
            int minRight2 = part2 == n2 ? int.MaxValue : nums2[part2];

            if (maxLeft1 <= minRight2 && maxLeft2 <= minRight1) {
                if ((n1 + n2) % 2 == 0) {
                    return (Math.Max(maxLeft1, maxLeft2) + Math.Min(minRight1, minRight2)) / 2.0;
                } else {
                    return Math.Max(maxLeft1, maxLeft2);
                }
            } else if (maxLeft1 > minRight2) {
                right = part1 - 1;
            } else {
                left = part1 + 1;
            }
        }
        throw new ArgumentException();
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