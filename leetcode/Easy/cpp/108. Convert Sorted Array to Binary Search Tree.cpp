/*
https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Convert Sorted Array to Binary Search Tree".
*/

class Solution {
public:
    TreeNode* sortedArrayToBST(vector<int>& nums) {
        return build(nums, 0, nums.size() - 1);
    }

private:
    TreeNode* build(const vector<int>& nums, int l, int r) {
        if (l > r) return nullptr;

        int mid = l + (r - l) / 2;
        TreeNode* root = new TreeNode(nums[mid]);

        root->left  = build(nums, l, mid - 1);
        root->right = build(nums, mid + 1, r);

        return root;
    }
};
