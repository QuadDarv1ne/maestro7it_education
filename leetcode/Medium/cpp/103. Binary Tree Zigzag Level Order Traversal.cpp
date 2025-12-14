/*
https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

// struct TreeNode {
//     int val;
//     TreeNode *left, *right;
//     TreeNode(int x): val(x), left(nullptr), right(nullptr) {}
// };

class Solution {
public:
    vector<vector<int>> zigzagLevelOrder(TreeNode* root) {
        /*
        Решение задачи "Binary Tree Zigzag Level Order Traversal" (LeetCode 103).

        Идея:
        - BFS по уровням.
        - Переменная flip чередует направление.
        */
        vector<vector<int>> result;
        if (!root) return result;

        vector<TreeNode*> current{root};
        bool flip = false;

        while (!current.empty()) {
            vector<int> vals;
            vector<TreeNode*> nextLevel;

            for (TreeNode* node : current) {
                vals.push_back(node->val);
                if (node->left) nextLevel.push_back(node->left);
                if (node->right) nextLevel.push_back(node->right);
            }

            if (flip) reverse(vals.begin(), vals.end());
            result.push_back(vals);

            current = move(nextLevel);
            flip = !flip;
        }

        return result;
    }
};
