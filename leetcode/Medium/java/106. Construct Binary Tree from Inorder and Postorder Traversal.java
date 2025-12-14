/*
https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

class Solution {
    public TreeNode buildTree(int[] inorder, int[] postorder) {
        if (postorder.length == 0) return null;

        int rootVal = postorder[postorder.length - 1];
        TreeNode root = new TreeNode(rootVal);

        int idx = 0;
        for (; idx < inorder.length; idx++) {
            if (inorder[idx] == rootVal) break;
        }

        int[] leftIn = Arrays.copyOfRange(inorder, 0, idx);
        int[] rightIn = Arrays.copyOfRange(inorder, idx + 1, inorder.length);
        int[] leftPost = Arrays.copyOfRange(postorder, 0, idx);
        int[] rightPost = Arrays.copyOfRange(postorder, idx, postorder.length - 1);

        root.left = buildTree(leftIn, leftPost);
        root.right = buildTree(rightIn, rightPost);

        return root;
    }
}
