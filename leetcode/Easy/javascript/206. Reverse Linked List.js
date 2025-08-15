/**
 * https://leetcode.com/problems/reverse-linked-list/
 */

/**
 * Переворачивает односвязный список.
 * 
 * Алгоритм:
 * 1. prev = null (новая голова)
 * 2. current = head
 * 3. nextNode = current.next
 * 4. current.next = prev
 * 5. prev = current, current = nextNode
 * 6. Возвращаем prev
 * 
 * Время: O(n)
 * Память: O(1)
 */

// function ListNode(val, next = null) {
//     this.val = val;
//     this.next = next;
// }

var reverseList = function(head) {
    let prev = null;
    let current = head;
    while (current) {
        let nextNode = current.next;
        current.next = prev;
        prev = current;
        current = nextNode;
    }
    return prev;
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