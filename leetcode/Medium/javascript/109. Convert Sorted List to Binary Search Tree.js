/*
https://leetcode.com/problems/convert-sorted-list-to-binary-search-tree/

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Convert Sorted List to Binary Search Tree".
*/

// Definition for singly-linked list and tree node assumed provided by LeetCode

var sortedListToBST = function(head) {
    // Сначала считаем длину списка
    let n = 0;
    let node = head;
    while (node) {
        n++;
        node = node.next;
    }

    let curr = head;

    function build(left, right) {
        if (left > right) return null;

        const mid = Math.floor((left + right) / 2);

        const leftNode = build(left, mid - 1);

        const root = new TreeNode(curr.val);
        curr = curr.next;

        root.left = leftNode;
        root.right = build(mid + 1, right);

        return root;
    }

    return build(0, n - 1);
};
