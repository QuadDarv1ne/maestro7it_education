/*
https://leetcode.com/problems/binary-tree-inorder-traversal/description/

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
    vector<int> inorderTraversal(TreeNode* root) {
        /*
        Решение задачи "Binary Tree Inorder Traversal" (LeetCode 94).

        Идея:
        - Итеративно с помощью стека проходим
          левую часть, затем корень и правую.
        */
        vector<int> res;
        stack<TreeNode*> st;
        TreeNode* curr = root;

        while (curr || !st.empty()) {
            while (curr) {
                st.push(curr);
                curr = curr->left;
            }
            curr = st.top(); st.pop();
            res.push_back(curr->val);
            curr = curr->right;
        }
        return res;
    }
};
