/**
 * https://leetcode.com/problems/median-of-two-sorted-arrays/description/
 */

/**
 * @brief Находит медиану двух отсортированных массивов за O(log(min(m,n))).
 *
 * Алгоритм:
 * - Берём меньший массив для бинарного поиска (nums1 длины n1, nums2 длины n2).
 * - Ищем partition в nums1, вычисляем соответствующее partition во втором массиве.
 * - Определяем maxLeft и minRight на каждой стороне.
 * - Если допустимо разделение (maxLeft1 ≤ minRight2 && maxLeft2 ≤ minRight1),
 *   вычисляем медиану (с учётом чётности суммы длин).
 * - Иначе сдвигаем границы бинарного поиска.
 *
 * Сложность:
 * - Время: O(log(min(m, n)))  
 * - Память: O(1)
 *
 * @param nums1 первый отсортированный массив
 * @param nums2 второй отсортированный массив
 * @return медиана как double
 */
#include <vector>
#include <algorithm>
#include <climits>
using namespace std;

class Solution {
public:
    double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
        int n1 = nums1.size();
        int n2 = nums2.size();
        // Всегда бинарный поиск по меньшему массиву
        if (n1 > n2) return findMedianSortedArrays(nums2, nums1);

        int left = 0, right = n1;
        while (left <= right) {
            int part1 = (left + right) / 2;
            int part2 = (n1 + n2 + 1) / 2 - part1;

            int maxLeft1 = part1 == 0 ? INT_MIN : nums1[part1 - 1];
            int minRight1 = part1 == n1 ? INT_MAX : nums1[part1];

            int maxLeft2 = part2 == 0 ? INT_MIN : nums2[part2 - 1];
            int minRight2 = part2 == n2 ? INT_MAX : nums2[part2];

            if (maxLeft1 <= minRight2 && maxLeft2 <= minRight1) {
                if ((n1 + n2) % 2 == 0) {
                    return (max(maxLeft1, maxLeft2) + min(minRight1, minRight2)) / 2.0;
                } else {
                    return static_cast<double>(max(maxLeft1, maxLeft2));
                }
            } else if (maxLeft1 > minRight2) {
                right = part1 - 1;
            } else {
                left = part1 + 1;
            }
        }
        return 0.0; // Теоретически сюда не дойдём
    }
};

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