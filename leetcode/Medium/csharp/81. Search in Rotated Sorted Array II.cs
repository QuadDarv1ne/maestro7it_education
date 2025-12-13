/*
https://leetcode.com/problems/search-in-rotated-sorted-array-ii/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

public class Solution {
    public bool Search(int[] nums, int target) {
        /*
        Решение задачи "Search in Rotated Sorted Array II" (LeetCode 81).

        Идея:
        - Модифицированный бинарный поиск.
        - При nums[left] == nums[mid] сдвигаем левую границу.
        - Анализируем отсортированную половину.

        Сложность:
        - Время: O(log n) / O(n)
        - Память: O(1)
        */
        int left = 0, right = nums.Length - 1;

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
