/**
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
 */

/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    /**
     * @brief Сортирует связный список с использованием алгоритма сортировки вставками
     * 
     * Алгоритм сортировки вставками для связного списка:
     * 1. Создаем фиктивный узел-заглушку для нового отсортированного списка
     * 2. Итеративно берем каждый узел из исходного списка
     * 3. Вставляем его в правильную позицию в отсортированном списке
     * 4. Повторяем до тех пор, пока все узлы не будут отсортированы
     * 
     * Сложность: O(n²) время, O(1) память
     * 
     * @param head Указатель на голову несортированного списка
     * @return ListNode* Указатель на голову отсортированного списка
     */
    ListNode* insertionSortList(ListNode* head) {
        if (!head || !head->next) return head;
        
        // Создаем фиктивный узел для нового отсортированного списка
        ListNode* dummy = new ListNode(0);
        ListNode* curr = head;  // Текущий узел для вставки
        
        while (curr) {
            // Сохраняем следующий узел перед изменением связей
            ListNode* next = curr->next;
            ListNode* prev = dummy;  // Предыдущий узел для поиска позиции вставки
            
            // Находим позицию для вставки в отсортированном списке
            while (prev->next && prev->next->val < curr->val) {
                prev = prev->next;
            }
            
            // Вставляем curr между prev и prev->next
            curr->next = prev->next;
            prev->next = curr;
            
            // Переходим к следующему узлу в исходном списке
            curr = next;
        }
        
        ListNode* sortedHead = dummy->next;
        delete dummy;
        return sortedHead;
    }
};