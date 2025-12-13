/*
https://leetcode.com/problems/binary-tree-inorder-traversal/description/

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

var inorderTraversal = function(root) {
    /*
    Решение задачи "Binary Tree Inorder Traversal" (LeetCode 94).

    Идея:
    - Стек для хранения узлов.
    - Обходим сначала все левые ветки,
      затем обрабатываем корень и правую ветку.
    */
    const res = [];
    const stack = [];
    let curr = root;

    while (curr || stack.length) {
        while (curr) {
            stack.push(curr);
            curr = curr.left;
        }
        curr = stack.pop();
        res.push(curr.val);
        curr = curr.right;
    }

    return res;
};
