/**
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
 */

/**
 * Definition for singly-linked list.
 */
class ListNode {
    val: number;
    next: ListNode | null;
    constructor(val?: number, next?: ListNode | null) {
        this.val = val === undefined ? 0 : val;
        this.next = next === undefined ? null : next;
    }
}

function insertGreatestCommonDivisors(head: ListNode | null): ListNode | null {
    const gcd = (a: number, b: number): number => {
        while (b !== 0) {
            [a, b] = [b, a % b];
        }
        return a;
    };

    let current = head;

    while (current && current.next) {
        const gcdValue = gcd(current.val, current.next.val);
        const newNode = new ListNode(gcdValue, current.next);
        current.next = newNode;
        current = newNode.next;
    }

    return head;
};