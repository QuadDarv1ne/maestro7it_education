/*
https://leetcode.com/problems/search-in-rotated-sorted-array-ii/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

class Solution {
    public boolean search(int[] nums, int target) {
        /*
        Решение задачи "Search in Rotated Sorted Array II" (LeetCode 81).

        Идея:
        - Используем бинарный поиск с обработкой дубликатов.
        - Если nums[left] == nums[mid], двигаем левый указатель.
        - Проверяем отсортированную часть массива.

        Сложность:
        - Время: O(log n) / O(n)
        - Память: O(1)
        */
        int left = 0, right = nums.length - 1;

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
}
