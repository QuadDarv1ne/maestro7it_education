/*
https://leetcode.com/problems/convert-sorted-list-to-binary-search-tree/

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Convert Sorted List to Binary Search Tree".
*/

class Solution {
    private ListNode curr;

    public TreeNode sortedListToBST(ListNode head) {
        int n = 0;
        curr = head;
        ListNode p = head;
        while (p != null) {
            n++;
            p = p.next;
        }
        return build(0, n - 1);
    }

    private TreeNode build(int left, int right) {
        if (left > right) return null;

        int mid = (left + right) / 2;

        TreeNode leftNode = build(left, mid - 1);

        TreeNode root = new TreeNode(curr.val);
        curr = curr.next;

        root.left = leftNode;
        root.right = build(mid + 1, right);
        return root;
    }
}
