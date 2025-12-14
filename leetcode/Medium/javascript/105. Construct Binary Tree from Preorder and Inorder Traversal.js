/*
https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

/**
 * Definition for a binary tree node.
 * function TreeNode(val, left, right) {
 *     this.val = (val===undefined ? 0 : val)
 *     this.left = (left===undefined ? null : left)
 *     this.right = (right===undefined ? null : right)
 * }
 */

var buildTree = function(preorder, inorder) {
    if (!preorder.length) return null;

    let rootVal = preorder[0];
    let root = new TreeNode(rootVal);

    let idx = inorder.indexOf(rootVal);

    root.left = buildTree(preorder.slice(1, 1+idx), inorder.slice(0, idx));
    root.right = buildTree(preorder.slice(1+idx), inorder.slice(idx+1));

    return root;
};
