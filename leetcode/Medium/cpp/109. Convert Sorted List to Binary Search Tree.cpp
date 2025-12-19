/*
https://leetcode.com/problems/convert-sorted-list-to-binary-search-tree/

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Convert Sorted List to Binary Search Tree".
*/

// LeetCode уже предоставляет ListNode и TreeNode

class Solution {
public:
    ListNode* curr;

    TreeNode* build(int left, int right) {
        if (left > right) return nullptr;

        int mid = (left + right) / 2;
        TreeNode* leftNode = build(left, mid - 1);

        TreeNode* root = new TreeNode(curr->val);
        curr = curr->next;

        root->left = leftNode;
        root->right = build(mid + 1, right);
        return root;
    }

    TreeNode* sortedListToBST(ListNode* head) {
        int n = 0;
        curr = head;
        for (ListNode* p = head; p; p = p->next) n++;

        return build(0, n - 1);
    }
};
