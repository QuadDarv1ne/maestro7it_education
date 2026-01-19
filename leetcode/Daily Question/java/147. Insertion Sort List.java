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
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode() {}
 *     ListNode(int val) { this.val = val; }
 *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
 * }
 */
class Solution {
    /**
     * @brief Сортирует связный список с использованием алгоритма сортировки вставками
     * 
     * @param head Голова несортированного списка
     * @return ListNode Голова отсортированного списка
     */
    public ListNode insertionSortList(ListNode head) {
        if (head == null || head.next == null) return head;
        
        // Создаем фиктивный узел для нового отсортированного списка
        ListNode dummy = new ListNode(0);
        ListNode curr = head;
        
        while (curr != null) {
            // Сохраняем следующий узел
            ListNode next = curr.next;
            ListNode prev = dummy;
            
            // Находим позицию для вставки
            while (prev.next != null && prev.next.val < curr.val) {
                prev = prev.next;
            }
            
            // Вставляем узел
            curr.next = prev.next;
            prev.next = curr;
            
            // Переходим к следующему узлу
            curr = next;
        }
        
        return dummy.next;
    }
}