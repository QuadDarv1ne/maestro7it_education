/*
https://leetcode.com/problems/binary-tree-level-order-traversal-ii/description/

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Binary Tree Level Order Traversal II".
*/

var levelOrderBottom = function(root) {
    if (!root) return [];

    let queue = [root];
    let result = [];

    while (queue.length > 0) {
        let n = queue.length;
        let level = [];

        for (let i = 0; i < n; i++) {
            let node = queue.shift();
            level.push(node.val);
            if (node.left)  queue.push(node.left);
            if (node.right) queue.push(node.right);
        }
        result.push(level);
    }

    return result.reverse();
};
