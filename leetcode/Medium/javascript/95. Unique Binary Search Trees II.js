/*
https://leetcode.com/problems/unique-binary-search-trees-ii/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

/**
 * Definition for a binary tree node.
 * function TreeNode(val, left, right) {
 *     this.val = (val===undefined ? 0 : val)
 *     this.left = (left===undefined ? null : left)
 *     this.right = (right===undefined ? null : right)
 * }
 */

var generateTrees = function(n) {
    /*
    Решение задачи "Unique Binary Search Trees II" (LeetCode 95).

    Идея:
    - Рекурсивная функция build генерирует
      все BST на отрезке [start..end].
    */
    if (n === 0) return [];

    function build(start, end) {
        const trees = [];
        if (start > end) {
            trees.push(null);
            return trees;
        }
        for (let i = start; i <= end; i++) {
            const leftTrees = build(start, i - 1);
            const rightTrees = build(i + 1, end);
            for (const l of leftTrees) {
                for (const r of rightTrees) {
                    const root = new TreeNode(i, l, r);
                    trees.push(root);
                }
            }
        }
        return trees;
    }

    return build(1, n);
};
