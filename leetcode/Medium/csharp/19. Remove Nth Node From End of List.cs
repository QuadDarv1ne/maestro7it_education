/**
 * https://leetcode.com/problems/remove-nth-node-from-end-of-list/description/
 */

/// <summary>
/// Удаляет n-й узел с конца односвязного списка.
/// Алгоритм:
/// - Используется фиктивная голова dummy
/// - Два указателя: fast и slow
/// - fast передвигается на n+1 шаг вперёд
/// - Двигаем оба указателя, пока fast != null
/// - slow.next — узел для удаления
/// Время: O(L), Память: O(1)
/// </summary>
public class Solution {
    public ListNode RemoveNthFromEnd(ListNode head, int n) {
        ListNode dummy = new ListNode(0);
        dummy.next = head;
        ListNode fast = dummy;
        ListNode slow = dummy;

        for (int i = 0; i <= n; i++) {
            fast = fast.next;
        }

        while (fast != null) {
            fast = fast.next;
            slow = slow.next;
        }

        slow.next = slow.next.next;
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