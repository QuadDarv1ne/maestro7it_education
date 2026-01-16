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