/*
https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

public class Solution {
    public TreeNode BuildTree(int[] inorder, int[] postorder) {
        if (postorder.Length == 0) return null;

        int rootVal = postorder[^1];
        TreeNode root = new TreeNode(rootVal);

        int idx = Array.IndexOf(inorder, rootVal);

        root.left = BuildTree(inorder[0..idx], postorder[0..idx]);
        root.right = BuildTree(inorder[(idx+1)..], postorder[idx..^1]);

        return root;
    }
}
