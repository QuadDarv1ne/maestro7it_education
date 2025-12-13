/*
https://leetcode.com/problems/remove-duplicates-from-sorted-list-ii/description/

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
    public ListNode DeleteDuplicates(ListNode head) {
        /*
        Решение задачи "Remove Duplicates from Sorted List II" (LeetCode 82).

        Идея:
        - Заводим dummy перед началом списка.
        - Сканируем список, пропуская все дубликаты.
        - Подхватываем только уникальные значения.

        Сложность:
        - Время: O(n)
        - Память: O(1)
        */
        ListNode dummy = new ListNode(0, head);
        ListNode prev = dummy;
        ListNode curr = head;

        while (curr != null && curr.next != null) {
            if (curr.val == curr.next.val) {
                int dup = curr.val;
                while (curr != null && curr.val == dup) {
                    curr = curr.next;
                }
                prev.next = curr;
            } else {
                prev = curr;
                curr = curr.next;
            }
        }

        return dummy.next;
    }
}
