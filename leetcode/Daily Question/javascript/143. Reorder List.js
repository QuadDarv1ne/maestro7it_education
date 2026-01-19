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
 * @param {ListNode} head
 * @return {void} Do not return anything, modify head in-place instead.
 * 
 * @brief Переупорядочивает связный список в порядке L0→Ln→L1→Ln-1→L2→Ln-2→...
 * 
 * Алгоритм:
 * 1. Находим середину списка с помощью быстрого и медленного указателей
 * 2. Разделяем список на две половины
 * 3. Реверсируем вторую половину
 * 4. Сливаем две половины, чередуя узлы
 */
var reorderList = function(head) {
    if (!head || !head.next || !head.next.next) return;
    
    // Шаг 1: Находим середину списка
    let slow = head;
    let fast = head;
    
    while (fast.next && fast.next.next) {
        slow = slow.next;
        fast = fast.next.next;
    }
    
    // Шаг 2: Разделяем список на две половины
    let secondHalf = slow.next;
    slow.next = null;
    
    // Шаг 3: Реверсируем вторую половину
    let prev = null;
    let curr = secondHalf;
    
    while (curr) {
        let next = curr.next;
        curr.next = prev;
        prev = curr;
        curr = next;
    }
    secondHalf = prev;
    
    // Шаг 4: Сливаем две половины
    let first = head;
    let second = secondHalf;
    
    while (second) {
        let temp1 = first.next;
        let temp2 = second.next;
        
        first.next = second;
        second.next = temp1;
        
        first = temp1;
        second = temp2;
    }
};