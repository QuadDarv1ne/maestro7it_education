/*
https://leetcode.com/problems/recover-binary-search-tree/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

// struct TreeNode {
//     int val;
//     TreeNode *left;
//     TreeNode *right;
//     TreeNode(): val(0), left(nullptr), right(nullptr) {}
//     TreeNode(int x): val(x), left(nullptr), right(nullptr) {}
//     TreeNode(int x, TreeNode *l, TreeNode *r): val(x), left(l), right(r) {}
// };

class Solution {
private:
    TreeNode* first = nullptr;
    TreeNode* second = nullptr;
    TreeNode* prev = nullptr;

    void inorder(TreeNode* node) {
        if (!node) return;

        inorder(node->left);

        if (prev && prev->val > node->val) {
            if (!first) first = prev;
            second = node;
        }
        prev = node;

        inorder(node->right);
    }

public:
    void recoverTree(TreeNode* root) {
        inorder(root);
        // swap values
        int tmp = first->val;
        first->val = second->val;
        second->val = tmp;
    }
};
