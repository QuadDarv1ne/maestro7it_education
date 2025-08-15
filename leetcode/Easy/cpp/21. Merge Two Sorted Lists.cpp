/**
 * https://leetcode.com/problems/merge-two-sorted-lists/description/
 */

/**
 * Объединяет два отсортированных односвязных списка.
 *
 * Вход:
 *   - list1, list2 — указатели на головы списков.
 * Выход:
 *   - Указатель на голову объединённого списка.
 *
 * Алгоритм:
 *   - Использует фиктивную голову dummy и tail — текущий конец списка.
 *   - Пока оба не пусты, выбирается меньший узел.
 *   - После добавляем остаток непустого списка.
 *
 * Сложность:
 *   - Время: O(m + n)
 *   - Память: O(1)
 */
class Solution {
public:
    ListNode* mergeTwoLists(ListNode* l1, ListNode* l2) {
        ListNode dummy(0), *tail = &dummy;
        while (l1 && l2) {
            if (l1->val <= l2->val) {
                tail->next = l1;
                l1 = l1->next;
            } else {
                tail->next = l2;
                l2 = l2->next;
            }
            tail = tail->next;
        }
        tail->next = l1 ? l1 : l2;
        return dummy.next;
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