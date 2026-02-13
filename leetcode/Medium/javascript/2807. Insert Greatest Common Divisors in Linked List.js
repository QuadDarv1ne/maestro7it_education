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
 * function ListNode(val, next) {
 *     this.val = (val===undefined ? 0 : val)
 *     this.next = (next===undefined ? null : next)
 * }
 */

/**
 * @param {ListNode} head - Голова исходного связного списка.
 * @return {ListNode} - Голова списка после вставки узлов с НОД.
 */
var insertGreatestCommonDivisors = function(head) {
    // Вспомогательная функция для вычисления НОД (алгоритм Евклида)
    const gcd = (a, b) => {
        while (b !== 0) {
            [a, b] = [b, a % b];
        }
        return a;
    };

    let current = head;

    // Проходим по списку, пока есть хотя бы два узла для пары
    while (current && current.next) {
        const gcdValue = gcd(current.val, current.next.val);
        // Создаём новый узел со значением НОД, который будет указывать на next
        const newNode = new ListNode(gcdValue, current.next);
        // Текущий узел теперь указывает на новый узел
        current.next = newNode;
        // Перемещаем указатель на два узла вперёд (пропускаем вставленный)
        current = newNode.next;
    }

    return head;
};