/**
 * Соединение узлов произвольного бинарного дерева с правыми соседями
 * 
 * @param root Корень бинарного дерева
 * @return Модифицированное дерево с установленными next-указателями
 * 
 * Сложность: Время O(N), Память O(1)
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

// class Node {
//     public int val;
//     public Node left;
//     public Node right;
//     public Node next;
    
//     public Node() {}
//     public Node(int _val) {
//         val = _val;
//     }
//     public Node(int _val, Node _left, Node _right, Node _next) {
//         val = _val;
//         left = _left;
//         right = _right;
//         next = _next;
//     }
// }

class Solution {
    public Node connect(Node root) {
        if (root == null) return root;
        
        Node curr = root;
        
        while (curr != null) {
            // Dummy-узел для начала нового уровня
            Node dummy = new Node(0);
            Node tail = dummy;
            
            // Проходим по текущему уровню
            while (curr != null) {
                // Подсоединяем левого ребенка, если есть
                if (curr.left != null) {
                    tail.next = curr.left;
                    tail = tail.next;
                }
                
                // Подсоединяем правого ребенка, если есть
                if (curr.right != null) {
                    tail.next = curr.right;
                    tail = tail.next;
                }
                
                // Переходим к следующему узлу на текущем уровне
                curr = curr.next;
            }
            
            // Переходим на следующий уровень
            curr = dummy.next;
        }
        
        return root;
    }
}