/*
https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    TreeNode* buildTree(vector<int>& inorder, vector<int>& postorder) {
        if (postorder.empty()) return nullptr;

        TreeNode* root = new TreeNode(postorder.back());
        postorder.pop_back();

        auto it = find(inorder.begin(), inorder.end(), root->val);
        int idx = distance(inorder.begin(), it);

        vector<int> leftIn(inorder.begin(), inorder.begin() + idx);
        vector<int> rightIn(inorder.begin() + idx + 1, inorder.end());
        vector<int> leftPost(postorder.begin(), postorder.begin() + idx);
        vector<int> rightPost(postorder.begin() + idx, postorder.end());

        root->left = buildTree(leftIn, leftPost);
        root->right = buildTree(rightIn, rightPost);

        return root;
    }
};
