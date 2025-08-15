/**
 * https://leetcode.com/problems/merge-two-sorted-lists/description/
 */
class Solution {
    /**
     * Объединяет два отсортированных односвязных списка.
     *
     * @param l1 голова первого списка
     * @param l2 голова второго списка
     * @return голова объединённого отсортированного списка
     *
     * Алгоритм:
     *  - Используем фиктивную голову dummy и tail.
     *  - Пока оба списка не пусты, добавляем меньший узел.
     *  - Затем присоединяем остаток.
     *
     * Сложность:
     *  - Время: O(m + n)
     *  - Память: O(1)
     */
    public ListNode mergeTwoLists(ListNode l1, ListNode l2) {
        ListNode dummy = new ListNode(0), tail = dummy;
        while (l1 != null && l2 != null) {
            if (l1.val <= l2.val) {
                tail.next = l1;
                l1 = l1.next;
            } else {
                tail.next = l2;
                l2 = l2.next;
            }
            tail = tail.next;
        }
        tail.next = (l1 != null) ? l1 : l2;
        return dummy.next;
    }
}

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