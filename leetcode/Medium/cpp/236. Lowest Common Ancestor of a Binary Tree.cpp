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
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode(int x) : val(x), left(NULL), right(NULL) {}
 * };
 */
class Solution {
public:
    /**
     * Находит наименьшего общего предка двух узлов в бинарном дереве.
     * 
     * Алгоритм (рекурсивный поиск):
     * 1. Если текущий узел равен p или q, возвращаем текущий узел.
     * 2. Рекурсивно ищем p и q в левом и правом поддеревьях.
     * 3. Если оба поддерева вернули не-null узлы, то текущий узел - LCA.
     * 4. Иначе возвращаем то, что не null (или null, если оба null).
     * 
     * Сложность:
     * Время: O(n)
     * Пространство: O(h) - высота дерева
     * 
     * @param root Корень бинарного дерева
     * @param p Первый узел
     * @param q Второй узел
     * @return Наименьший общий предок узлов p и q
     * 
     * Пример:
     * Входное дерево:
     *       3
     *     /   \
     *    5     1
     *   / \   / \
     *  6   2 0   8
     *     / \
     *    7   4
     * 
     * p = 5, q = 1 → LCA = 3
     * p = 5, q = 4 → LCA = 5
     */
    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
        // Базовый случай: пустой узел или нашли p или q
        if (!root || root == p || root == q) {
            return root;
        }
        
        // Рекурсивно ищем в левом и правом поддеревьях
        TreeNode* left = lowestCommonAncestor(root->left, p, q);
        TreeNode* right = lowestCommonAncestor(root->right, p, q);
        
        // Если оба поддерева вернули не-null, текущий узел - LCA
        if (left && right) {
            return root;
        }
        
        // Иначе возвращаем то, что не null
        return left ? left : right;
    }
    
    /**
     * Итеративное решение с использованием стека и родительских указателей.
     * 
     * Алгоритм:
     * 1. Используем стек для обхода дерева.
     * 2. Строим словарь родительских указателей.
     * 3. Находим пути от p и q к корню.
     * 4. Находим пересечение путей.
     * 
     * Сложность:
     * Время: O(n)
     * Пространство: O(n)
     */
    TreeNode* lowestCommonAncestorIterative(TreeNode* root, TreeNode* p, TreeNode* q) {
        if (!root) return nullptr;
        
        stack<TreeNode*> stk;
        unordered_map<TreeNode*, TreeNode*> parent;
        
        stk.push(root);
        parent[root] = nullptr;
        
        // Обходим дерево, пока не найдем оба узла
        while (parent.find(p) == parent.end() || parent.find(q) == parent.end()) {
            TreeNode* node = stk.top();
            stk.pop();
            
            if (node->left) {
                parent[node->left] = node;
                stk.push(node->left);
            }
            if (node->right) {
                parent[node->right] = node;
                stk.push(node->right);
            }
        }
        
        // Находим всех предков узла p
        unordered_set<TreeNode*> ancestors;
        while (p) {
            ancestors.insert(p);
            p = parent[p];
        }
        
        // Находим первого общего предка узла q
        while (ancestors.find(q) == ancestors.end()) {
            q = parent[q];
        }
        
        return q;
    }
};