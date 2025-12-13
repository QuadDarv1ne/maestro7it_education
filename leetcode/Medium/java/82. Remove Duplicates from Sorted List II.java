/*
https://leetcode.com/problems/remove-duplicates-from-sorted-list-ii/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

// public class ListNode {
//     int val;
//     ListNode next;
//     ListNode() {}
//     ListNode(int val) { this.val = val; }
//     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
// }

class Solution {
    public ListNode deleteDuplicates(ListNode head) {
        /*
        Решение задачи "Remove Duplicates from Sorted List II" (LeetCode 82).

        Идея:
        - Используем фиктивный узел перед списком.
        - Пропускаем группы узлов с одинаковыми значениями.
        - prev указывает на последний уникальный узел.
        
        Сложность:
        - Время: O(n)
        - Память: O(1)
        */
        ListNode dummy = new ListNode(0, head);
        ListNode prev = dummy;
        ListNode curr = head;

        while (curr != null && curr.next != null) {
            if (curr.val == curr.next.val) {
                int dupVal = curr.val;
                while (curr != null && curr.val == dupVal) {
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
