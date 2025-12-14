/*
https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

public class Solution {
    public TreeNode BuildTree(int[] preorder, int[] inorder) {
        if (preorder.Length == 0) return null;

        TreeNode root = new TreeNode(preorder[0]);
        int idx = Array.IndexOf(inorder, preorder[0]);

        root.left = BuildTree(
            preorder[1..(1+idx)],
            inorder[0..idx]
        );
        root.right = BuildTree(
            preorder[(1+idx)..],
            inorder[(idx+1)..]
        );

        return root;
    }
}
