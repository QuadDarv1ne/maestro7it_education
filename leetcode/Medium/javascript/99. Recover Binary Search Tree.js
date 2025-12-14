/*
https://leetcode.com/problems/recover-binary-search-tree/description/

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
var recoverTree = function(root) {
    let first = null;
    let second = null;
    let prev = null;

    function inorder(node) {
        if (!node) return;

        inorder(node.left);

        if (prev && prev.val > node.val) {
            if (!first) first = prev;
            second = node;
        }
        prev = node;

        inorder(node.right);
    }

    inorder(root);

    // swap values
    const tmp = first.val;
    first.val = second.val;
    second.val = tmp;
};
