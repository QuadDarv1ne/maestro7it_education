/**
 * https://leetcode.com/problems/merge-two-sorted-lists/description/
 */

/// <summary>
/// Объединяет два отсортированных односвязных списка в один.
/// </summary>
/// <param name="l1">Голова первого списка.</param>
/// <param name="l2">Голова второго списка.</param>
/// <returns>Голова нового отсортированного списка.</returns>
/// <remarks>
/// Используется фиктивный узел (dummy) и tail для построения результата.
/// Время: O(m + n), память: O(1).
/// </remarks>

public class Solution {
    public ListNode MergeTwoLists(ListNode list1, ListNode list2) {
        ListNode dummy = new ListNode();
        ListNode tail = dummy;

        while (list1 != null && list2 != null) {
            if (list1.val < list2.val) {
                tail.next = list1;
                list1 = list1.next;
            } else {
                tail.next = list2;
                list2 = list2.next;
            }
            tail = tail.next;
        }

        if (list1 != null) tail.next = list1;
        if (list2 != null) tail.next = list2;

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