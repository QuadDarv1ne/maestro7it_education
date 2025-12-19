/*
https://leetcode.com/problems/binary-tree-level-order-traversal-ii/description/

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Binary Tree Level Order Traversal II".
*/

class Solution {
public:
    vector<vector<int>> levelOrderBottom(TreeNode* root) {
        if (!root) return {};

        queue<TreeNode*> q;
        q.push(root);
        vector<vector<int>> result;

        while (!q.empty()) {
            int sz = q.size();
            vector<int> level;
            for (int i = 0; i < sz; i++) {
                TreeNode* node = q.front();
                q.pop();
                level.push_back(node->val);
                if (node->left)  q.push(node->left);
                if (node->right) q.push(node->right);
            }
            result.push_back(level);
        }

        reverse(result.begin(), result.end());
        return result;
    }
};
