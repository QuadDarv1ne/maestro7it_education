/*
https://leetcode.com/problems/reverse-linked-list-ii/description/

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

var reverseBetween = function(head, left, right) {
    /*
    Решение задачи "Reverse Linked List II" (LeetCode 92).

    Идея:
    - dummy для удобства.
    - Доходим до узла перед left.
    - Переворачиваем участок [left,right] в месте.
    */
    let dummy = new ListNode(0, head);
    let prev = dummy;

    for (let i = 0; i < left - 1; i++)
        prev = prev.next;

    let curr = prev.next;
    for (let i = 0; i < right - left; i++) {
        let temp = curr.next;
        curr.next = temp.next;
        temp.next = prev.next;
        prev.next = temp;
    }

    return dummy.next;
};
