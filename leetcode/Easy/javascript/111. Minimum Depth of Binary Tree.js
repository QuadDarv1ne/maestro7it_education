/*
https://leetcode.com/problems/minimum-depth-of-binary-tree/

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Minimum Depth of Binary Tree"
с использованием BFS.
*/

var minDepth = function(root) {
    if (!root) return 0;

    let queue = [[root, 1]];

    while (queue.length > 0) {
        let [node, depth] = queue.shift();

        if (!node.left && !node.right)
            return depth;

        if (node.left)
            queue.push([node.left, depth + 1]);
        if (node.right)
            queue.push([node.right, depth + 1]);
    }
    return 0;
};
