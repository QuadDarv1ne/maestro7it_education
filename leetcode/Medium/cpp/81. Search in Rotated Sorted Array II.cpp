/*
https://leetcode.com/problems/search-in-rotated-sorted-array-ii/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

class Solution {
public:
    bool search(vector<int>& nums, int target) {
        /*
        Решение задачи "Search in Rotated Sorted Array II" (LeetCode 81).

        Идея:
        - Используем модифицированный бинарный поиск.
        - Если nums[left] == nums[mid], невозможно определить
          упорядоченную часть — сдвигаем left.
        - Определяем, какая половина отсортирована,
          и проверяем, может ли там быть target.

        Сложность:
        - Время: O(log n) в среднем, O(n) в худшем случае
        - Память: O(1)
        */
        int left = 0, right = nums.size() - 1;

        while (left <= right) {
            int mid = left + (right - left) / 2;

            if (nums[mid] == target)
                return true;

            if (nums[left] == nums[mid]) {
                left++;
                continue;
            }

            if (nums[left] < nums[mid]) {
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
        return false;
    }
};
