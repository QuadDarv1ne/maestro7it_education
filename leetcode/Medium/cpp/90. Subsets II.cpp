/*
https://leetcode.com/problems/subsets-ii/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

class Solution {
public:
    vector<vector<int>> subsetsWithDup(vector<int>& nums) {
        /*
        Решение задачи "Subsets II" (LeetCode 90).

        Идея:
        - Сортируем массив для удобного пропуска дубликатов.
        - Используем рекурсивный backtracking.
        - Пропускаем одинаковые элементы на одном уровне.

        Сложность:
        - Время: O(2^n * n)
        - Память: O(2^n * n)
        */
        sort(nums.begin(), nums.end());
        vector<vector<int>> res;
        vector<int> path;
        backtrack(nums, 0, path, res);
        return res;
    }

private:
    void backtrack(vector<int>& nums, int start, vector<int>& path, vector<vector<int>>& res) {
        res.push_back(path);
        for (int i = start; i < nums.size(); i++) {
            if (i > start && nums[i] == nums[i-1]) continue;
            path.push_back(nums[i]);
            backtrack(nums, i+1, path, res);
            path.pop_back();
        }
    }
};
