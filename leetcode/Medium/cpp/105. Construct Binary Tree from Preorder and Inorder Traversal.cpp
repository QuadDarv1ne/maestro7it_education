/*
https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

#include <vector>
using namespace std;

class Solution {
public:
    TreeNode* buildTree(vector<int>& preorder, vector<int>& inorder) {
        if (preorder.empty()) return nullptr;

        TreeNode* root = new TreeNode(preorder[0]);

        auto it = find(inorder.begin(), inorder.end(), preorder[0]);
        int idx = distance(inorder.begin(), it);

        vector<int> leftPre(preorder.begin()+1, preorder.begin()+1+idx);
        vector<int> rightPre(preorder.begin()+1+idx, preorder.end());
        vector<int> leftIn(inorder.begin(), inorder.begin()+idx);
        vector<int> rightIn(inorder.begin()+idx+1, inorder.end());

        root->left = buildTree(leftPre, leftIn);
        root->right = buildTree(rightPre, rightIn);

        return root;
    }
};
