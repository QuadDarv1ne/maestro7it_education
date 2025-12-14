/*
https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

public class Solution {
    public IList<IList<int>> ZigzagLevelOrder(TreeNode root) {
        /*
        Решение задачи "Binary Tree Zigzag Level Order Traversal" (LeetCode 103).

        Идея:
        - Обычный BFS.
        - Чередуем порядок обхода.
        */
        var result = new List<IList<int>>();
        if (root == null) return result;

        var current = new List<TreeNode>{ root };
        bool flip = false;

        while (current.Count > 0) {
            var vals = new List<int>();
            var nextLevel = new List<TreeNode>();

            foreach (var node in current) {
                vals.Add(node.val);
                if (node.left != null) nextLevel.Add(node.left);
                if (node.right != null) nextLevel.Add(node.right);
            }

            if (flip) vals.Reverse();
            result.Add(vals);

            current = nextLevel;
            flip = !flip;
        }

        return result;
    }
}
