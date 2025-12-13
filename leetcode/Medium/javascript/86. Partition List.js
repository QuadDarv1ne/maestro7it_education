/*
https://leetcode.com/problems/partition-list/description/

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

var partition = function(head, x) {
    /*
    Решение задачи "Partition List" (LeetCode 86).

    Идея:
    - Два списка: узлы < x и узлы ≥ x.
    - Сохраняем оригинальный порядок.
    - В конце склеиваем.

    Сложность:
    - Время: O(n)
    - Память: O(1)
    */
    let beforeHead = new ListNode(0);
    let afterHead = new ListNode(0);

    let before = beforeHead;
    let after = afterHead;

    let curr = head;
    while (curr) {
        if (curr.val < x) {
            before.next = curr;
            before = before.next;
        } else {
            after.next = curr;
            after = after.next;
        }
        curr = curr.next;
    }

    after.next = null;
    before.next = afterHead.next;
    return beforeHead.next;
};
