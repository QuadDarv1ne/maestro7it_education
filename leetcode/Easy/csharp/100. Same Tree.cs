/*
https://leetcode.com/problems/same-tree/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

public class Solution {
    public bool IsSameTree(TreeNode p, TreeNode q) {
        /*
        Идея:
        - Если оба узла null — одинаковы.
        - Если один null — не одинаковы.
        - Иначе сравниваем значения и рекурсивно левое/правое.
        */
        if (p == null && q == null) return true;
        if (p == null || q == null) return false;
        if (p.val != q.val) return false;
        return IsSameTree(p.left, q.left) && IsSameTree(p.right, q.right);
    }
}
