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

/*
// Definition for a Node.
class Node {
    int val;
    Node next;
    Node random;

    public Node(int val) {
        this.val = val;
        this.next = null;
        this.random = null;
    }
}
*/

class Solution {
    public Node copyRandomList(Node head) {
        /**
         * Создает глубокую копию связанного списка с random указателями.
         * 
         * Алгоритм (HashMap):
         * 1. Создаем HashMap для отображения оригинальных узлов на копии
         * 2. Первый проход: создаем все копии узлов
         * 3. Второй проход: устанавливаем next и random связи
         * 
         * Сложность: O(n) время, O(n) память
         */
        
        if (head == null) {
            return null;
        }
        
        // HashMap для отображения оригинальных узлов на копии
        Map<Node, Node> nodeMap = new HashMap<>();
        
        // Первый проход: создаем копии всех узлов
        Node current = head;
        while (current != null) {
            nodeMap.put(current, new Node(current.val));
            current = current.next;
        }
        
        // Второй проход: устанавливаем связи
        current = head;
        while (current != null) {
            // Устанавливаем next связь
            if (current.next != null) {
                nodeMap.get(current).next = nodeMap.get(current.next);
            }
            
            // Устанавливаем random связь
            if (current.random != null) {
                nodeMap.get(current).random = nodeMap.get(current.random);
            }
            
            current = current.next;
        }
        
        return nodeMap.get(head);
    }
}