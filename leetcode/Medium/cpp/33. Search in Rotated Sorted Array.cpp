/**
 * https://leetcode.com/problems/search-in-rotated-sorted-array/description/
 */

#include <vector>
using namespace std;

class Solution {
public:
    /**
     * Выполняет бинарный поиск элемента target в вращённом отсортированном массиве nums.
     *
     * @param nums Вектор целых чисел, отсортированный по возрастанию и затем вращённый.
     * @param target Целое число, которое нужно найти.
     * @return Индекс элемента target, или -1, если элемент не найден.
     */
    int search(vector<int>& nums, int target) {
        int left = 0, right = nums.size() - 1;

        while (left <= right) {
            int mid = left + (right - left) / 2;

            if (nums[mid] == target) return mid;

            // Определяем, какая часть отсортирована
            if (nums[left] <= nums[mid]) {
                if (nums[left] <= target && target < nums[mid])
                    right = mid - 1;
                else
                    left = mid + 1;
            } else {
                if (nums[mid] < target && target <= nums[right])
                    left = mid + 1;
                else
                    right = mid - 1;
            }
        }

        return -1; // Элемент не найден
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