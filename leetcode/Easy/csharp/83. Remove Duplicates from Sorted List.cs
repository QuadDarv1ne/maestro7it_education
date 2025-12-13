/*
https://leetcode.com/problems/remove-duplicates-from-sorted-list/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

// public class ListNode {
//     public int val;
//     public ListNode next;
//     public ListNode(int val = 0, ListNode next = null) {
//         this.val = val;
//         this.next = next;
//     }
// }

public class Solution {
    public ListNode DeleteDuplicates(ListNode head) {
        /*
        Решение задачи "Remove Duplicates from Sorted List" (LeetCode 83).

        Идея:
        - Один проход по списку.
        - При совпадении значений пропускаем следующий узел.

        Сложность:
        - Время: O(n)
        - Память: O(1)
        */
        ListNode curr = head;

        while (curr != null && curr.next != null) {
            if (curr.val == curr.next.val)
                curr.next = curr.next.next;
            else
                curr = curr.next;
        }
        return head;
    }
}
