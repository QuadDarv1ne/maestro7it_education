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
 *     ListNode(int x) { val = x; }
 * }
 */
class Solution {
    /**
     * Удаляет узел из односвязного списка без доступа к голове списка.
     * 
     * Алгоритм:
     * 1. Копирует значение следующего узла в текущий узел.
     * 2. Изменяет указатель текущего узел на узел через один.
     * 
     * Сложность:
     * Время: O(1)
     * Пространство: O(1)
     * 
     * @param node Узел, который нужно удалить из списка
     * 
     * Пример:
     * Исходный список: 4 -> 5 -> 1 -> 9
     * Удаляем узел со значением 5
     * Результат: 4 -> 1 -> 9
     * 
     * Примечание:
     * - Узел не является хвостовым (гарантируется, что node.next != null)
     * - В Java не нужно явно освобождать память
     */
    public void deleteNode(ListNode node) {
        // Копируем значение следующего узла в текущий узел
        node.val = node.next.val;
        
        // Пропускаем следующий узел
        node.next = node.next.next;
        
        // В Java сборщик мусора удалит старый следующий узел
    }
    
    /**
     * Альтернативная реализация с явным сохранением следующего узла.
     * 
     * @param node Узел для удаления
     */
    public void deleteNodeAlternative(ListNode node) {
        // Проверяем, что узел не является null и не хвостовым
        if (node == null || node.next == null) {
            return;
        }
        
        // Получаем следующий узел
        ListNode nextNode = node.next;
        
        // Копируем значение и указатель
        node.val = nextNode.val;
        node.next = nextNode.next;
        
        // Обнуляем ссылку для помощи сборщику мусора
        nextNode.next = null;
    }
}