/*
https://leetcode.com/problems/swap-nodes-in-pairs/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X  
GitHub: https://github.com/QuadDarv1ne/  
*/

/**
 * Definition for singly-linked list.
 * function ListNode(val, next) {
 *     this.val = (val===undefined ? 0 : val)
 *     this.next = (next===undefined ? null : next)
 * }
 */

/**
 * @param {ListNode} head
 * @return {ListNode}
 */
var swapPairs = function(head) {
    const dummy = new ListNode(0);
    dummy.next = head;
    let prev = dummy;

    while (head && head.next) {
        const first = head;
        const second = head.next;

        // Перестановка
        prev.next = second;
        first.next = second.next;
        second.next = first;

        // Подготовка к следующей паре
        prev = first;
        head = first.next;
    }

    return dummy.next;
};

/*
''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/
