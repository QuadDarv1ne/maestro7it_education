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

public class Solution {
    /// <summary>
    /// Находит максимальную сумму "близнецов" в связном списке.
    /// Близнецы: i-й элемент с начала и i-й с конца.
    /// </summary>
    /// <param name="head">Голова односвязного списка четной длины.</param>
    /// <returns>Максимальная сумма пары близнецов.</returns>
    public int PairSum(ListNode head) {
        ListNode slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        
        ListNode prev = null, curr = slow;
        while (curr != null) {
            ListNode nextTemp = curr.next;
            curr.next = prev;
            prev = curr;
            curr = nextTemp;
        }
        
        int maxSum = 0;
        ListNode first = head, second = prev;
        while (second != null) {
            maxSum = Math.Max(maxSum, first.val + second.val);
            first = first.next;
            second = second.next;
        }
        
        return maxSum;
    }
}