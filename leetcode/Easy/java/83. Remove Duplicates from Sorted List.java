/*
https://leetcode.com/problems/remove-duplicates-from-sorted-list/description/

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
        Решение задачи "Remove Duplicates from Sorted List" (LeetCode 83).

        Идея:
        - Последовательно сравниваем текущий и следующий узлы.
        - При совпадении значений удаляем следующий узел.

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
