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
 * @return {ListNode}
 * 
 * @brief Сортирует связный список с использованием алгоритма сортировки вставками
 */
var insertionSortList = function(head) {
    if (!head || !head.next) return head;
    
    // Создаем фиктивный узел для нового отсортированного списка
    const dummy = new ListNode(0);
    let curr = head;
    
    while (curr) {
        // Сохраняем следующий узел
        const next = curr.next;
        let prev = dummy;
        
        // Находим позицию для вставки
        while (prev.next && prev.next.val < curr.val) {
            prev = prev.next;
        }
        
        // Вставляем узел
        curr.next = prev.next;
        prev.next = curr;
        
        // Переходим к следующему узлу
        curr = next;
    }
    
    return dummy.next;
};