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
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    /**
     * Инвертирует бинарное дерево, меняя местами левые и правые поддеревья для каждого узла.
     * 
     * Алгоритм (рекурсивный):
     * 1. Базовый случай: если узел пустой (nullptr), возвращаем nullptr.
     * 2. Рекурсивно инвертируем левое поддерево.
     * 3. Рекурсивно инвертируем правое поддерево.
     * 4. Меняем местами левый и правый потомков текущего узла.
     * 5. Возвращаем текущий узел.
     * 
     * Сложность:
     * Время: O(n), где n - количество узлов в дереве
     * Пространство: O(h), где h - высота дерева (глубина рекурсии)
     * 
     * @param root Корень бинарного дерева
     * @return Корень инвертированного дерева
     * 
     * Пример:
     * Входное дерево:
     *       4
     *     /   \
     *    2     7
     *   / \   / \
     *  1   3 6   9
     * 
     * Выходное дерево:
     *       4
     *     /   \
     *    7     2
     *   / \   / \
     *  9   6 3   1
     */
    TreeNode* invertTree(TreeNode* root) {
        // Базовый случай: пустой узел
        if (!root) {
            return nullptr;
        }
        
        // Рекурсивно инвертируем поддеревья
        TreeNode* left_inverted = invertTree(root->left);
        TreeNode* right_inverted = invertTree(root->right);
        
        // Меняем местами потомков
        root->left = right_inverted;
        root->right = left_inverted;
        
        return root;
    }
    
    /**
     * Итеративная версия инвертирования бинарного дерева.
     * 
     * Алгоритм (BFS):
     * 1. Используем очередь для обхода дерева по уровням.
     * 2. Для каждого узла меняем местами его левого и правого потомков.
     * 3. Добавляем потомков в очередь (если они существуют).
     * 
     * Сложность:
     * Время: O(n)
     * Пространство: O(w), где w - максимальная ширина дерева
     * 
     * @param root Корень бинарного дерева
     * @return Корень инвертированного дерева
     */
    TreeNode* invertTreeIterative(TreeNode* root) {
        if (!root) {
            return nullptr;
        }
        
        queue<TreeNode*> q;
        q.push(root);
        
        while (!q.empty()) {
            TreeNode* node = q.front();
            q.pop();
            
            // Меняем местами левого и правого потомков
            swap(node->left, node->right);
            
            // Добавляем потомков в очередь, если они существуют
            if (node->left) {
                q.push(node->left);
            }
            if (node->right) {
                q.push(node->right);
            }
        }
        
        return root;
    }
};