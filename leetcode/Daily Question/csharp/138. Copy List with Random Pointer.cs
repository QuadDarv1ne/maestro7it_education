/*
// Definition for a Node.
public class Node {
    public int val;
    public Node next;
    public Node random;
    
    public Node(int _val) {
        val = _val;
        next = null;
        random = null;
    }
}
*/

public class Solution {
    public Node CopyRandomList(Node head) {
        /**
         * Создает глубокую копию связанного списка с random указателями.
         * 
         * Алгоритм (HashMap):
         * 1. Создаем Dictionary для отображения оригинальных узлов на копии
         * 2. Первый проход: создаем все копии узлов
         * 3. Второй проход: устанавливаем next и random связи
         * 
         * Сложность: O(n) время, O(n) память
         */
        
        if (head == null) {
            return null;
        }
        
        // Dictionary для отображения оригинальных узлов на копии
        Dictionary<Node, Node> nodeDict = new Dictionary<Node, Node>();
        
        // Первый проход: создаем копии всех узлов
        Node current = head;
        while (current != null) {
            nodeDict[current] = new Node(current.val);
            current = current.next;
        }
        
        // Второй проход: устанавливаем связи
        current = head;
        while (current != null) {
            // Устанавливаем next связь
            if (current.next != null) {
                nodeDict[current].next = nodeDict[current.next];
            }
            
            // Устанавливаем random связь
            if (current.random != null) {
                nodeDict[current].random = nodeDict[current.random];
            }
            
            current = current.next;
        }
        
        return nodeDict[head];
    }
}