/**
 * https://leetcode.com/problems/remove-nth-node-from-end-of-list/description/
 */

/**
 * Удаляет n-й узел с конца односвязного списка.
 * Алгоритм:
 * - Используется фиктивная голова dummy
 * - Два указателя: fast и slow
 * - fast передвигается на n+1 шаг вперёд
 * - Двигаем оба указателя до конца
 * - slow.next — узел для удаления
 * Время: O(L), Память: O(1)
 * @param {ListNode} head — голова списка
 * @param {number} n — номер узла с конца
 * @return {ListNode} — голова обновлённого списка
 */
var removeNthFromEnd = function(head, n) {
    let dummy = new ListNode(0);
    dummy.next = head;
    let fast = dummy;
    let slow = dummy;

    for (let i = 0; i <= n; i++) {
        fast = fast.next;
    }

    while (fast) {
        fast = fast.next;
        slow = slow.next;
    }

    slow.next = slow.next.next;
    return dummy.next;
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