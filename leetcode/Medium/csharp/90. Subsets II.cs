/*
https://leetcode.com/problems/subsets-ii/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

public class Solution {
    public IList<IList<int>> SubsetsWithDup(int[] nums) {
        /*
        Решение задачи "Subsets II" (LeetCode 90).

        Идея:
        - Сортируем массив, используем рекурсивный backtracking.
        - Пропускаем повторяющиеся элементы на одном уровне.
        */
        Array.Sort(nums);
        var res = new List<IList<int>>();
        Backtrack(nums, 0, new List<int>(), res);
        return res;
    }

    private void Backtrack(int[] nums, int start, List<int> path, List<IList<int>> res) {
        res.Add(new List<int>(path));
        for (int i = start; i < nums.Length; i++) {
            if (i > start && nums[i] == nums[i-1]) continue;
            path.Add(nums[i]);
            Backtrack(nums, i+1, path, res);
            path.RemoveAt(path.Count-1);
        }
    }
}
