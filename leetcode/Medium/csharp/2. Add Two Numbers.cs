/**
 * https://leetcode.com/problems/add-two-numbers/description/
 */

/**
 * Определение узла связанного списка (уже определено в LeetCode, не нужно переопределять).
 * public class ListNode {
 *     public int val;
 *     public ListNode next;
 *     public ListNode(int val=0, ListNode next=null) {
 *         this.val = val;
 *         this.next = next;
 *     }
 * }
 */

public class Solution {
    /**
     * Складывает два числа, представленных связанными списками, где цифры
     * хранятся в обратном порядке.
     * Возвращает сумму в виде связанного списка.
     * 
     * @param l1 Первый связанный список, представляющий первое число.
     * @param l2 Второй связанный список, представляющий второе число.
     * @return Связанный список, представляющий сумму двух чисел.
     */
    public ListNode AddTwoNumbers(ListNode l1, ListNode l2) {
        ListNode dummy = new ListNode(0); // Вспомогательный узел для результата
        ListNode current = dummy;
        int carry = 0; // Перенос из старшего разряда

        while (l1 != null || l2 != null || carry != 0) {
            int val1 = (l1 != null) ? l1.val : 0; // Значение из первого списка или 0
            int val2 = (l2 != null) ? l2.val : 0; // Значение из второго списка или 0

            int sum = val1 + val2 + carry; // Сумма текущих цифр и переноса
            carry = sum / 10; // Обновляем перенос
            current.next = new ListNode(sum % 10); // Создаём новый узел с текущей цифрой
            current = current.next; // Переходим к следующему узлу

            if (l1 != null) l1 = l1.next; // Переход к следующему элементу первого списка
            if (l2 != null) l2 = l2.next; // Переход к следующему элементу второго списка
        }

        return dummy.next; // Возвращаем результат, пропуская вспомогательный узел
    }
}

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