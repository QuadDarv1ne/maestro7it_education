/*
https://leetcode.com/problems/remove-duplicates-from-sorted-list-ii/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

class Solution {
public:
    ListNode* deleteDuplicates(ListNode* head) {
        /*
        Решение задачи "Remove Duplicates from Sorted List II" (LeetCode 82).

        Идея:
        - Используем фиктивный узел (dummy) перед головой списка.
        - Два указателя: prev — последний подтверждённый уникальный узел,
          curr — текущий для обхода.
        - Если curr->val == curr->next->val, пропускаем все узлы с этим значением.
        - В конце возвращаем dummy->next.

        Сложность:
        - Время: O(n)
        - Память: O(1)
        */
        ListNode* dummy = new ListNode(0, head);
        ListNode* prev = dummy;
        ListNode* curr = head;
        
        while (curr && curr->next) {
            if (curr->val == curr->next->val) {
                int dupVal = curr->val;
                while (curr && curr->val == dupVal) {
                    curr = curr->next;
                }
                prev->next = curr;
            } else {
                prev = curr;
                curr = curr->next;
            }
        }
        
        return dummy->next;
    }
};
