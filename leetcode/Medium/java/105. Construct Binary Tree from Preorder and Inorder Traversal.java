/*
https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

class Solution {
    public TreeNode buildTree(int[] preorder, int[] inorder) {
        if (preorder.length == 0) return null;

        TreeNode root = new TreeNode(preorder[0]);

        int idx = 0;
        for (; idx < inorder.length; idx++) {
            if (inorder[idx] == preorder[0]) break;
        }

        int[] leftPre = Arrays.copyOfRange(preorder, 1, 1 + idx);
        int[] rightPre = Arrays.copyOfRange(preorder, 1 + idx, preorder.length);
        int[] leftIn = Arrays.copyOfRange(inorder, 0, idx);
        int[] rightIn = Arrays.copyOfRange(inorder, idx + 1, inorder.length);

        root.left = buildTree(leftPre, leftIn);
        root.right = buildTree(rightPre, rightIn);

        return root;
    }
}
