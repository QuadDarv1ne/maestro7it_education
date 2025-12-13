/*
https://leetcode.com/problems/unique-binary-search-trees-ii/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

public class TreeNode {
    int val;
    TreeNode left, right;
    TreeNode() {}
    TreeNode(int val) { this.val = val; }
    TreeNode(int val, TreeNode left, TreeNode right) {
        this.val = val;
        this.left = left;
        this.right = right;
    }
}

class Solution {
    public List<TreeNode> generateTrees(int n) {
        /*
        Решение задачи "Unique Binary Search Trees II" (LeetCode 95).

        Идея:
        - Рекурсивная функция Build генерирует
          все BST на отрезке [start..end].
        */
        List<TreeNode> result = new ArrayList<>();
        if (n == 0) return result;
        return build(1, n);
    }

    private List<TreeNode> build(int start, int end) {
        List<TreeNode> trees = new ArrayList<>();
        if (start > end) {
            trees.add(null);
            return trees;
        }
        for (int i = start; i <= end; i++) {
            List<TreeNode> leftTrees = build(start, i - 1);
            List<TreeNode> rightTrees = build(i + 1, end);
            for (TreeNode l : leftTrees) {
                for (TreeNode r : rightTrees) {
                    TreeNode root = new TreeNode(i, l, r);
                    trees.add(root);
                }
            }
        }
        return trees;
    }
}
