/*
https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/description/

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

var buildTree = function(inorder, postorder) {
    if (!postorder.length) return null;

    let rootVal = postorder[postorder.length - 1];
    let root = new TreeNode(rootVal);

    let idx = inorder.indexOf(rootVal);

    root.left = buildTree(inorder.slice(0, idx), postorder.slice(0, idx));
    root.right = buildTree(inorder.slice(idx+1), postorder.slice(idx, -1));

    return root;
};
