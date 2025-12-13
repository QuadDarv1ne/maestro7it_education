/*
https://leetcode.com/problems/search-in-rotated-sorted-array-ii/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

var search = function(nums, target) {
    /*
    Решение задачи "Search in Rotated Sorted Array II" (LeetCode 81).

    Идея:
    - Модифицированный бинарный поиск.
    - Дубликаты мешают определению порядка —
      при nums[left] == nums[mid] сдвигаем left.
    - Работаем только с отсортированной половиной.

    Сложность:
    - Время: O(log n) / O(n)
    - Память: O(1)
    */
    let left = 0, right = nums.length - 1;

    while (left <= right) {
        let mid = Math.floor((left + right) / 2);

        if (nums[mid] === target)
            return true;

        if (nums[left] === nums[mid]) {
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
};
