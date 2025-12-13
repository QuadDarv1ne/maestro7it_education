/*
https://leetcode.com/problems/remove-duplicates-from-sorted-list/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

// struct ListNode {
//     int val;
//     ListNode *next;
//     ListNode() : val(0), next(nullptr) {}
//     ListNode(int x) : val(x), next(nullptr) {}
//     ListNode(int x, ListNode *next) : val(x), next(next) {}
// };

class Solution {
public:
    ListNode* deleteDuplicates(ListNode* head) {
        /*
        Решение задачи "Remove Duplicates from Sorted List" (LeetCode 83).

        Идея:
        - Проходим по списку один раз.
        - Если значение текущего узла совпадает со следующим,
          пропускаем следующий узел.
        - В итоге в списке остаётся по одному элементу каждого значения.

        Сложность:
        - Время: O(n)
        - Память: O(1)
        */
        ListNode* curr = head;

        while (curr && curr->next) {
            if (curr->val == curr->next->val)
                curr->next = curr->next->next;
            else
                curr = curr->next;
        }
        return head;
    }
};
