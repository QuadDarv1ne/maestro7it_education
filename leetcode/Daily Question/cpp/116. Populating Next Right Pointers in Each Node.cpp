/**
 * Соединение узлов совершенного бинарного дерева с правыми соседями
 * 
 * @param root Корень совершенного бинарного дерева
 * @return Модифицированное дерево с установленными next-указателями
 * 
 * Сложность: Время O(N), Память O(1)
 * 
 * Алгоритм:
 * 1. Используем три указателя: leftmost, curr, prev
 * 2. Проходим по дереву уровень за уровнем
 * 3. На каждом уровне соединяем узлы следующего уровня
 * 4. Переходим на следующий уровень через левого ребенка
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
        
        Node* leftmost = root;
        
        // Проходим по уровням
        while (leftmost->left) {
            Node* curr = leftmost;
            
            // Соединяем узлы текущего уровня
            while (curr) {
                // Соединяем левого ребенка с правым ребенком
                curr->left->next = curr->right;
                
                // Соединяем правого ребенка с левым ребенком следующего узла
                if (curr->next) {
                    curr->right->next = curr->next->left;
                }
                
                // Переходим к следующему узлу на текущем уровне
                curr = curr->next;
            }
            
            // Переходим на следующий уровень
            leftmost = leftmost->left;
        }
        
        return root;
    }
};