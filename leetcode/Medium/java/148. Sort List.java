/**
 * Решение задачи сортировки связного списка методом итеративного слияния (bottom-up merge sort).
 * <p>
 * Алгоритм:
 * 1. Подсчитывается длина списка.
 * 2. Используется фиктивная голова (dummy node) для удобства обработки.
 * 3. Внешний цикл по шагам (step), начиная с 1, удваивая step на каждой итерации, пока step < n.
 * 4. Внутри цикла список разбивается на блоки длиной step, которые затем попарно сливаются.
 * 5. После каждого прохода по всему списку получаем частично отсортированный список, который будет обработан на следующем шаге с удвоенным размером блока.
 * 6. Процесс продолжается до тех пор, пока размер блока не станет больше или равен длине списка.
 * <p>
 * Особенности:
 * - Временная сложность: O(n log n)
 * - Пространственная сложность: O(1) (без учета рекурсии, итеративный подход)
 */
class Solution {
    /**
     * Сортирует связный список в порядке возрастания.
     *
     * @param head головной узел связного списка
     * @return головной узел отсортированного списка
     */
    public ListNode sortList(ListNode head) {
        if (head == null || head.next == null) {
            return head;
        }
        
        int n = 0;
        ListNode node = head;
        while (node != null) {
            n++;
            node = node.next;
        }
        
        ListNode dummy = new ListNode(0);
        dummy.next = head;
        
        for (int step = 1; step < n; step *= 2) {
            ListNode prev = dummy;
            ListNode curr = dummy.next;
            
            while (curr != null) {
                ListNode left = curr;
                ListNode right = split(left, step);
                curr = split(right, step);
                
                ListNode merged = merge(left, right);
                prev.next = merged;
                
                while (prev.next != null) {
                    prev = prev.next;
                }
            }
        }
        
        return dummy.next;
    }
    
    /**
     * Разделяет связный список на два блока заданного размера.
     * Первый блок будет состоять из первых `step` узлов (или меньше, если список короче).
     * Возвращает голову второго блока (т.е. узел, следующий за последним узлом первого блока).
     * При этом первый блок отрезается от исходного списка.
     *
     * @param head головной узел списка, который нужно разделить
     * @param step размер первого блока
     * @return голова второго блока (или null, если второго блока нет)
     */
    private ListNode split(ListNode head, int step) {
        if (head == null) {
            return null;
        }
        
        ListNode cur = head;
        for (int i = 1; i < step && cur.next != null; i++) {
            cur = cur.next;
        }
        
        ListNode nextBlock = cur.next;
        cur.next = null;
        return nextBlock;
    }
    
    /**
     * Объединяет два отсортированных связных списка в один отсортированный список.
     * В процессе слияния создается новый фиктивный узел, к которому последовательно
     * присоединяются узлы из обоих списков в порядке возрастания.
     *
     * @param l1 головной узел первого отсортированного списка
     * @param l2 головной узел второго отсортированного списка
     * @return головной узел объединенного отсортированного списка
     */
    private ListNode merge(ListNode l1, ListNode l2) {
        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        
        while (l1 != null && l2 != null) {
            if (l1.val <= l2.val) {
                tail.next = l1;
                l1 = l1.next;
            } else {
                tail.next = l2;
                l2 = l2.next;
            }
            tail = tail.next;
        }
        
        if (l1 != null) {
            tail.next = l1;
        }
        if (l2 != null) {
            tail.next = l2;
        }
        
        return dummy.next;
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