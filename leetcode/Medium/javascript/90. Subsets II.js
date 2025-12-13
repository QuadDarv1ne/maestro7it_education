/*
https://leetcode.com/problems/subsets-ii/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

var subsetsWithDup = function(nums) {
    /*
    Решение задачи "Subsets II" (LeetCode 90).

    Идея:
    - Сортируем массив для пропуска дубликатов.
    - Backtracking для построения всех подмножеств.
    */
    nums.sort((a,b) => a-b);
    const res = [];

    const backtrack = (start, path) => {
        res.push([...path]);
        for (let i = start; i < nums.length; i++) {
            if (i > start && nums[i] === nums[i-1]) continue;
            path.push(nums[i]);
            backtrack(i+1, path);
            path.pop();
        }
    };

    backtrack(0, []);
    return res;
};
