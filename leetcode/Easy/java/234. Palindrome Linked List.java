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
     * Проверяет, является ли односвязный список палиндромом.
     * 
     * Алгоритм:
     * 1. Находит середину списка с помощью быстрого и медленного указателей.
     * 2. Разворачивает вторую половину списка.
     * 3. Сравнивает первую и развернутую вторую половины.
     * 4. Восстанавливает исходный список.
     * 
     * Сложность:
     * Время: O(n)
     * Пространство: O(1)
     * 
     * @param head Голова односвязного списка
     * @return true, если список является палиндромом, иначе false
     * 
     * Примеры:
     * Вход: 1->2->2->1
     * Выход: true
     * Вход: 1->2
     * Выход: false
     */
    public boolean isPalindrome(ListNode head) {
        if (head == null || head.next == null) {
            return true;
        }
        
        // Шаг 1: Находим середину списка
        ListNode slow = head;
        ListNode fast = head;
        
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        
        // Шаг 2: Разворачиваем вторую половину
        ListNode secondHalf = reverseList(slow);
        ListNode secondHalfCopy = secondHalf; // Для восстановления
        
        // Шаг 3: Сравниваем две половины
        ListNode firstHalf = head;
        boolean result = true;
        
        while (secondHalf != null) {
            if (firstHalf.val != secondHalf.val) {
                result = false;
                break;
            }
            firstHalf = firstHalf.next;
            secondHalf = secondHalf.next;
        }
        
        // Шаг 4: Восстанавливаем исходный список
        reverseList(secondHalfCopy);
        
        return result;
    }
    
    /**
     * Разворачивает односвязный список.
     * 
     * @param head Голова списка для разворота
     * @return Голова развернутого списка
     */
    private ListNode reverseList(ListNode head) {
        ListNode prev = null;
        ListNode current = head;
        
        while (current != null) {
            ListNode nextNode = current.next;
            current.next = prev;
            prev = current;
            current = nextNode;
        }
        
        return prev;
    }
    
    /**
     * Альтернативное решение с использованием ArrayList.
     * Проще, но использует O(n) дополнительной памяти.
     * 
     * @param head Голова списка
     * @return true, если список является палиндромом
     */
    public boolean isPalindromeWithArrayList(ListNode head) {
        List<Integer> values = new ArrayList<>();
        ListNode current = head;
        
        // Собираем значения в список
        while (current != null) {
            values.add(current.val);
            current = current.next;
        }
        
        // Проверяем, является ли список палиндромом
        int left = 0, right = values.size() - 1;
        while (left < right) {
            if (!values.get(left).equals(values.get(right))) {
                return false;
            }
            left++;
            right--;
        }
        
        return true;
    }
}