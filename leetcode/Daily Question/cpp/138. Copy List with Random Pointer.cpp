/*
// Definition for a Node.
class Node {
public:
    int val;
    Node* next;
    Node* random;
    
    Node(int _val) {
        val = _val;
        next = NULL;
        random = NULL;
    }
};
*/

class Solution {
public:
    Node* copyRandomList(Node* head) {
        /**
         * Создает глубокую копию связанного списка с random указателями.
         * 
         * Алгоритм (HashMap):
         * 1. Создаем unordered_map для отображения оригинальных узлов на копии
         * 2. Первый проход: создаем все копии узлов
         * 3. Второй проход: устанавливаем next и random связи
         * 
         * Сложность: O(n) время, O(n) память
         */
        
        if (!head) {
            return nullptr;
        }
        
        // unordered_map для отображения оригинальных узлов на копии
        unordered_map<Node*, Node*> nodeMap;
        
        // Первый проход: создаем копии всех узлов
        Node* current = head;
        while (current) {
            nodeMap[current] = new Node(current->val);
            current = current->next;
        }
        
        // Второй проход: устанавливаем связи
        current = head;
        while (current) {
            // Устанавливаем next связь
            if (current->next) {
                nodeMap[current]->next = nodeMap[current->next];
            }
            
            // Устанавливаем random связь
            if (current->random) {
                nodeMap[current]->random = nodeMap[current->random];
            }
            
            current = current->next;
        }
        
        return nodeMap[head];
    }
};