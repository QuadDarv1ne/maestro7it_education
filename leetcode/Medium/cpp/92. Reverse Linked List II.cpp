/*
https://leetcode.com/problems/reverse-linked-list-ii/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

// struct ListNode {
//     int val;
//     ListNode *next;
//     ListNode() : val(0), next(nullptr) {}
//     ListNode(int x) : val(x), next(nullptr) {}
//     ListNode(int x, ListNode* next) : val(x), next(next) {}
// };

class Solution {
public:
    ListNode* reverseBetween(ListNode* head, int left, int right) {
        /*
        Решение задачи "Reverse Linked List II" (LeetCode 92).

        Идея:
        - Используем фиктивный узел перед head.
        - Доходим до узла перед left.
        - Переворачиваем участок [left, right] в месте.
        */
        ListNode dummy(0, head);
        ListNode* prev = &dummy;

        for (int i = 0; i < left - 1; i++)
            prev = prev->next;

        ListNode* curr = prev->next;
        for (int i = 0; i < right - left; i++) {
            ListNode* temp = curr->next;
            curr->next = temp->next;
            temp->next = prev->next;
            prev->next = temp;
        }

        return dummy.next;
    }
};
