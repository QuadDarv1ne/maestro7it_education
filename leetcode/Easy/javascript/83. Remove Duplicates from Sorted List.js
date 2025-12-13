/*
https://leetcode.com/problems/remove-duplicates-from-sorted-list/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

/**
 * Definition for singly-linked list.
 * function ListNode(val, next) {
 *     this.val = (val===undefined ? 0 : val)
 *     this.next = (next===undefined ? null : next)
 * }
 */

var deleteDuplicates = function(head) {
    /*
    Решение задачи "Remove Duplicates from Sorted List" (LeetCode 83).

    Идея:
    - Линейный проход по списку.
    - Если значения совпадают — пропускаем следующий узел.

    Сложность:
    - Время: O(n)
    - Память: O(1)
    */
    let curr = head;

    while (curr && curr.next) {
        if (curr.val === curr.next.val)
            curr.next = curr.next.next;
        else
            curr = curr.next;
    }
    return head;
};
