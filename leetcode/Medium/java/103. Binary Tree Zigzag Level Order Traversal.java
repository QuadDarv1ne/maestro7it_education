/*
https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

class Solution {
    public List<List<Integer>> zigzagLevelOrder(TreeNode root) {
        /*
        Решение задачи "Binary Tree Zigzag Level Order Traversal" (LeetCode 103).

        Идея:
        - Проходим по каждому уровню.
        - Переменная flip меняет порядок.
        */
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) return result;

        List<TreeNode> current = new ArrayList<>();
        current.add(root);
        boolean flip = false;

        while (!current.isEmpty()) {
            List<Integer> vals = new ArrayList<>();
            List<TreeNode> nextLevel = new ArrayList<>();

            for (TreeNode node : current) {
                vals.add(node.val);
                if (node.left != null) nextLevel.add(node.left);
                if (node.right != null) nextLevel.add(node.right);
            }

            if (flip) Collections.reverse(vals);
            result.add(vals);

            current = nextLevel;
            flip = !flip;
        }
        return result;
    }
}
