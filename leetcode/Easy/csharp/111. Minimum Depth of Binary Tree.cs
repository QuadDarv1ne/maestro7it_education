/*
https://leetcode.com/problems/minimum-depth-of-binary-tree/

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Minimum Depth of Binary Tree"
через BFS: первый лист => min depth.
*/

public class Solution {
    public int MinDepth(TreeNode root) {
        if (root == null) return 0;

        var queue = new Queue<(TreeNode node, int depth)>();
        queue.Enqueue((root, 1));

        while (queue.Count > 0) {
            var (node, depth) = queue.Dequeue();

            if (node.left == null && node.right == null)
                return depth;

            if (node.left != null)
                queue.Enqueue((node.left, depth + 1));
            if (node.right != null)
                queue.Enqueue((node.right, depth + 1));
        }

        return 0;
    }
}
