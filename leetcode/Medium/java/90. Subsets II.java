/*
https://leetcode.com/problems/subsets-ii/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

class Solution {
    public List<List<Integer>> subsetsWithDup(int[] nums) {
        /*
        Решение задачи "Subsets II" (LeetCode 90).

        Идея:
        - Сортируем массив.
        - Backtracking с пропуском дубликатов.
        */
        Arrays.sort(nums);
        List<List<Integer>> res = new ArrayList<>();
        backtrack(nums, 0, new ArrayList<>(), res);
        return res;
    }

    private void backtrack(int[] nums, int start, List<Integer> path, List<List<Integer>> res) {
        res.add(new ArrayList<>(path));
        for (int i = start; i < nums.length; i++) {
            if (i > start && nums[i] == nums[i-1]) continue;
            path.add(nums[i]);
            backtrack(nums, i+1, path, res);
            path.remove(path.size()-1);
        }
    }
}
