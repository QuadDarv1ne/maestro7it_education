/**
 * https://leetcode.com/problems/linked-list-cycle/description/
 */

/**
 * Определяет, есть ли цикл в односвязном списке.
 * Алгоритм:
 * - slow двигается на 1 шаг, fast на 2 шага
 * - Если slow === fast, цикл найден
 * - Если fast === null или fast.next === null, цикла нет
 * Время: O(n), память: O(1)
 * @param {ListNode} head — голова списка
 * @return {boolean} true, если есть цикл; false — если нет
 */
var hasCycle = function(head) {
    if (!head || !head.next) return false;
    let slow = head;
    let fast = head.next;
    while (fast && fast.next) {
        if (slow === fast) return true;
        slow = slow.next;
        fast = fast.next.next;
    }
    return false;
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