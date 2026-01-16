/**
 * Соединение узлов произвольного бинарного дерева с правыми соседями
 * 
 * @param root Корень бинарного дерева
 * @return Модифицированное дерево с установленными next-указателями
 * 
 * Сложность: Время O(N), Память O(1)
 * 
 * Алгоритм:
 * 1. Используем dummy-узел для начала каждого уровня
 * 2. Для каждого уровня проходим по узлам через next
 * 3. Подсоединяем существующих детей к tail
 * 4. Переходим на следующий уровень
 * 
 * Автор: Дуплей Максим Игоревич
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 */

// class Node {
// public:
//     int val;
//     Node* left;
//     Node* right;
//     Node* next;

//     Node() : val(0), left(NULL), right(NULL), next(NULL) {}
//     Node(int _val) : val(_val), left(NULL), right(NULL), next(NULL) {}
//     Node(int _val, Node* _left, Node* _right, Node* _next)
//         : val(_val), left(_left), right(_right), next(_next) {}
// };

class Solution {
public:
    Node* connect(Node* root) {
        if (!root) return root;
        
        Node* curr = root;
        
        while (curr) {
            // Dummy-узел для начала нового уровня
            Node dummy(0);
            Node* tail = &dummy;
            
            // Проходим по текущему уровню
            while (curr) {
                // Подсоединяем левого ребенка, если есть
                if (curr->left) {
                    tail->next = curr->left;
                    tail = tail->next;
                }
                
                // Подсоединяем правого ребенка, если есть
                if (curr->right) {
                    tail->next = curr->right;
                    tail = tail->next;
                }
                
                // Переходим к следующему узлу на текущем уровне
                curr = curr->next;
            }
            
            // Переходим на следующий уровень
            curr = dummy.next;
        }
        
        return root;
    }
};