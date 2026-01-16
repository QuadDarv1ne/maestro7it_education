/**
 * https://leetcode.com/problems/copy-list-with-random-pointer/description/
 * 
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
 * // Definition for a Node.
 * function Node(val, next, random) {
 *    this.val = val;
 *    this.next = next;
 *    this.random = random;
 * };
 */

/**
 * @param {Node} head
 * @return {Node}
 */
var copyRandomList = function(head) {
    /**
     * Создает глубокую копию связанного списка с random указателями.
     * 
     * Алгоритм (HashMap):
     * 1. Создаем Map для отображения оригинальных узлов на копии
     * 2. Первый проход: создаем все копии узлов
     * 3. Второй проход: устанавливаем next и random связи
     * 
     * Сложность: O(n) время, O(n) память
     */
    
    if (!head) {
        return null;
    }
    
    // Map для отображения оригинальных узлов на копии
    const nodeMap = new Map();
    
    // Первый проход: создаем копии всех узлов
    let current = head;
    while (current) {
        nodeMap.set(current, new Node(current.val));
        current = current.next;
    }
    
    // Второй проход: устанавливаем связи
    current = head;
    while (current) {
        // Устанавливаем next связь
        if (current.next) {
            nodeMap.get(current).next = nodeMap.get(current.next);
        }
        
        // Устанавливаем random связь
        if (current.random) {
            nodeMap.get(current).random = nodeMap.get(current.random);
        }
        
        current = current.next;
    }
    
    return nodeMap.get(head);
};