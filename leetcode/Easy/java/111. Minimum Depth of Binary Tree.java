/*
https://leetcode.com/problems/minimum-depth-of-binary-tree/

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Minimum Depth of Binary Tree"
через BFS: как только найден лист — возвращаем.
*/

class Solution {
    public int minDepth(TreeNode root) {
        if (root == null) return 0;

        Queue<Pair<TreeNode, Integer>> queue = new ArrayDeque<>();
        queue.add(new Pair<>(root, 1));

        while (!queue.isEmpty()) {
            Pair<TreeNode, Integer> p = queue.poll();
            TreeNode node = p.getKey();
            int depth = p.getValue();

            if (node.left == null && node.right == null)
                return depth;

            if (node.left != null)
                queue.add(new Pair<>(node.left, depth + 1));
            if (node.right != null)
                queue.add(new Pair<>(node.right, depth + 1));
        }

        return 0;
    }
}
