/*
https://leetcode.com/problems/partition-list/description/

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
    public ListNode Partition(ListNode head, int x) {
        /*
        Решение задачи "Partition List" (LeetCode 86).

        Идея:
        - Два списка: один для < x, второй — ≥ x.
        - Сохраняем порядок, затем склеиваем.

        Сложность:
        - Время: O(n)
        - Память: O(1)
        */
        ListNode beforeHead = new ListNode(0);
        ListNode afterHead = new ListNode(0);
        ListNode before = beforeHead;
        ListNode after = afterHead;

        while (head != null) {
            if (head.val < x) {
                before.next = head;
                before = before.next;
            } else {
                after.next = head;
                after = after.next;
            }
            head = head.next;
        }

        after.next = null;
        before.next = afterHead.next;
        return beforeHead.next;
    }
}
