/*
https://leetcode.com/problems/reverse-linked-list-ii/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

// public class ListNode {
//     public int val;
//     public ListNode next;
//     public ListNode(int val=0, ListNode next=null) {
//         this.val = val;
//         this.next = next;
//     }
// }

public class Solution {
    public ListNode ReverseBetween(ListNode head, int left, int right) {
        /*
        Решение задачи "Reverse Linked List II" (LeetCode 92).

        Идея:
        - dummy перед списком.
        - Доходим до узла перед left.
        - Переставляем узлы для переворачивания участка [left,right].
        */
        ListNode dummy = new ListNode(0, head);
        ListNode prev = dummy;

        for (int i = 0; i < left - 1; i++)
            prev = prev.next;

        ListNode curr = prev.next;
        for (int i = 0; i < right - left; i++) {
            ListNode temp = curr.next;
            curr.next = temp.next;
            temp.next = prev.next;
            prev.next = temp;
        }

        return dummy.next;
    }
}
