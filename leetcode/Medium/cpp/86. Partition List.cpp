/*
https://leetcode.com/problems/partition-list/description/

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
    ListNode* partition(ListNode* head, int x) {
        /*
        Решение задачи "Partition List" (LeetCode 86).

        Идея:
        - Используем два фиктивных списка:
          меньших и больших/равных x.
        - Затем склеиваем списки.

        Сложность:
        - Время: O(n)
        - Память: O(1)
        */
        ListNode* before_head = new ListNode(0);
        ListNode* after_head = new ListNode(0);
        ListNode* before = before_head;
        ListNode* after = after_head;

        while (head) {
            if (head->val < x) {
                before->next = head;
                before = before->next;
            } else {
                after->next = head;
                after = after->next;
            }
            head = head->next;
        }

        after->next = nullptr;
        before->next = after_head->next;
        return before_head->next;
    }
};
