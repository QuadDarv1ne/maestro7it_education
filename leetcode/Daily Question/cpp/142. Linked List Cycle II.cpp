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
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */
class Solution {
public:
    /**
     * @brief Находит узел, с которого начинается цикл в связном списке
     * 
     * Алгоритм Флойда (черепаха и заяц):
     * 1. Используем два указателя: медленный (1 шаг) и быстрый (2 шага)
     * 2. Если указатели встречаются, значит есть цикл
     * 3. После встречи перемещаем один указатель в начало списка
     * 4. Двигаем оба указателя по одному шагу, пока они не встретятся
     * 5. Точка встречи - начало цикла
     * 
     * @param head Начало связного списка
     * @return ListNode* Узел начала цикла или nullptr, если цикла нет
     */
    ListNode *detectCycle(ListNode *head) {
        if (!head || !head->next) return nullptr;
        
        ListNode *slow = head;
        ListNode *fast = head;
        
        // Шаг 1: Находим точку встречи (если цикл существует)
        while (fast && fast->next) {
            slow = slow->next;
            fast = fast->next->next;
            
            if (slow == fast) {
                // Шаг 2: Находим начало цикла
                slow = head;
                while (slow != fast) {
                    slow = slow->next;
                    fast = fast->next;
                }
                return slow; // Начало цикла
            }
        }
        
        return nullptr; // Цикла нет
    }
};