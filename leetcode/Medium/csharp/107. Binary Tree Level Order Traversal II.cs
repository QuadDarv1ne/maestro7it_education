/*
https://leetcode.com/problems/binary-tree-level-order-traversal-ii/description/

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Binary Tree Level Order Traversal II".
*/

public class Solution {
    public IList<IList<int>> LevelOrderBottom(TreeNode root) {
        var result = new List<IList<int>>();
        if (root == null) return result;

        var queue = new Queue<TreeNode>();
        queue.Enqueue(root);

        while (queue.Count > 0) {
            int count = queue.Count;
            var level = new List<int>();

            for (int i = 0; i < count; i++) {
                TreeNode node = queue.Dequeue();
                level.Add(node.val);
                if (node.left != null) queue.Enqueue(node.left);
                if (node.right != null) queue.Enqueue(node.right);
            }

            result.Add(level);
        }

        result.Reverse();
        return result;
    }
}
