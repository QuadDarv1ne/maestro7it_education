/*
https://leetcode.com/problems/same-tree/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

class Solution {
public:
    bool isSameTree(TreeNode* p, TreeNode* q) {
        /*
        Решение задачи "Same Tree" (LeetCode 100).

        Идея:
        - Проверяем оба узла на NULL.
        - Если не NULL, сравниваем значения и рекурсивно левые/правые.
        */
        if (!p && !q) return true;
        if (!p || !q) return false;
        if (p->val != q->val) return false;
        return isSameTree(p->left, q->left) && isSameTree(p->right, q->right);
    }
};
