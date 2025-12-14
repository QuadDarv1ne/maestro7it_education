/*
https://leetcode.com/problems/recover-binary-search-tree/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

public class Solution {
    private TreeNode first = null;
    private TreeNode second = null;
    private TreeNode prev = null;

    public void RecoverTree(TreeNode root) {
        Inorder(root);

        // Меняем значения местами
        int temp = first.val;
        first.val = second.val;
        second.val = temp;
    }

    private void Inorder(TreeNode node) {
        if (node == null)
            return;

        Inorder(node.left);

        if (prev != null && prev.val > node.val) {
            if (first == null)
                first = prev;
            second = node;
        }

        prev = node;

        Inorder(node.right);
    }
}
