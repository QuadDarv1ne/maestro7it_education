/*
https://leetcode.com/problems/unique-binary-search-trees-ii/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

// struct TreeNode {
//     int val;
//     TreeNode *left;
//     TreeNode *right;
//     TreeNode() : val(0), left(nullptr), right(nullptr) {}
//     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
//     TreeNode(int x, TreeNode* l, TreeNode* r) : val(x), left(l), right(r) {}
// };

class Solution {
public:
    vector<TreeNode*> generateTrees(int n) {
        /*
        Решение задачи "Unique Binary Search Trees II" (LeetCode 95).

        Идея:
        - Рекурсивно строим все возможные BST
          на отрезке [start..end].
        */
        if (n == 0) return {};
        return build(1, n);
    }

private:
    vector<TreeNode*> build(int start, int end) {
        vector<TreeNode*> trees;
        if (start > end) {
            trees.push_back(nullptr);
            return trees;
        }
        for (int i = start; i <= end; ++i) {
            auto left_trees = build(start, i-1);
            auto right_trees = build(i+1, end);
            for (auto l : left_trees) {
                for (auto r : right_trees) {
                    TreeNode* root = new TreeNode(i);
                    root->left = l;
                    root->right = r;
                    trees.push_back(root);
                }
            }
        }
        return trees;
    }
};
