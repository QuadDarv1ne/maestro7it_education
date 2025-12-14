/*
https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/description/

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

var zigzagLevelOrder = function(root) {
    if (!root) return [];

    let result = [];
    let current = [root];
    let flip = false;

    while (current.length > 0) {
        let vals = [];
        let nextLevel = [];

        for (let node of current) {
            vals.push(node.val);
            if (node.left) nextLevel.push(node.left);
            if (node.right) nextLevel.push(node.right);
        }

        if (flip) vals.reverse();
        result.push(vals);

        current = nextLevel;
        flip = !flip;
    }

    return result;
};
