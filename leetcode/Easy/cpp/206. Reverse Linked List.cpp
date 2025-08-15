/**
 * https://leetcode.com/problems/reverse-linked-list/
 */

/**
 * Переворачивает односвязный список.
 * 
 * Алгоритм:
 * - prev = nullptr (новая голова)
 * - Проходим по списку:
 *   - сохраняем next_node = current->next
 *   - меняем current->next = prev
 *   - prev = current, current = next_node
 * 
 * Время: O(n)
 * Память: O(1)
 */

// struct ListNode {
//     int val;
//     ListNode *next;
//     ListNode(int x) : val(x), next(nullptr) {}
// };

class Solution {
public:
    ListNode* reverseList(ListNode* head) {
        ListNode* prev = nullptr;
        ListNode* current = head;
        while (current) {
            ListNode* next_node = current->next;
            current->next = prev;
            prev = current;
            current = next_node;
        }
        return prev;
    }
};

/*
''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/