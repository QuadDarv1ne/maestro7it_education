/*
https://leetcode.com/problems/remove-duplicates-from-sorted-list-ii/description/

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

/**
 * @param {ListNode} head
 * @return {ListNode}
 */
var deleteDuplicates = function(head) {
    /*
    Решение задачи "Remove Duplicates from Sorted List II" (LeetCode 82).

    Идея:
    - dummy перед началом списка для простого удаления головы.
    - Пропускаем подряд идущие значения, которые дублируются.
    - prev.next всегда указывает на следующий уникальный узел.

    Сложность:
    - Время: O(n)
    - Память: O(1)
    */
    let dummy = new ListNode(0, head);
    let prev = dummy;
    let curr = head;

    while (curr && curr.next) {
        if (curr.val === curr.next.val) {
            let dupVal = curr.val;
            while (curr && curr.val === dupVal) {
                curr = curr.next;
            }
            prev.next = curr;
        } else {
            prev = curr;
            curr = curr.next;
        }
    }
    return dummy.next;
};
