/**
 * https://leetcode.com/problems/reverse-linked-list/
 */

/// <summary>
/// Переворачивает односвязный список.
/// Алгоритм:
/// 1. prev = null
/// 2. Идём по списку с current
/// 3. Сохраняем nextNode = current.next
/// 4. Меняем current.next = prev
/// 5. prev = current, current = nextNode
/// 6. Возвращаем prev как новую голову
/// Время: O(n), Память: O(1)
/// </summary>

// public class ListNode {
//     public int val;
//     public ListNode next;
//     public ListNode(int val = 0, ListNode next = null) {
//         this.val = val;
//         this.next = next;
//     }
// }

public class Solution {
    public ListNode ReverseList(ListNode head) {
        ListNode prev = null;
        ListNode current = head;
        while (current != null) {
            ListNode nextNode = current.next;
            current.next = prev;
            prev = current;
            current = nextNode;
        }
        return prev;
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