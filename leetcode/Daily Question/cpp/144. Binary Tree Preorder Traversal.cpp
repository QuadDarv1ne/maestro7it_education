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

class Solution {
public:
    /**
     * @brief Итеративный предварительный обход бинарного дерева
     * 
     * Использует стек для эмуляции рекурсии:
     * 1. Помещаем корень в стек
     * 2. Пока стек не пуст:
     *    - Извлекаем вершину стека и добавляем её значение в результат
     *    - Помещаем правого потомка в стек (если существует)
     *    - Помещаем левого потомка в стек (если существует)
     * 
     * Сложность: O(n) время, O(n) память
     * 
     * @param root Корень бинарного дерева
     * @return vector<int> Вектор значений узлов в порядке preorder
     */
    vector<int> preorderTraversal(TreeNode* root) {
        vector<int> result;
        if (root == nullptr) return result;
        
        stack<TreeNode*> nodeStack;
        nodeStack.push(root);
        
        while (!nodeStack.empty()) {
            TreeNode* node = nodeStack.top();
            nodeStack.pop();
            
            result.push_back(node->val);
            
            // Сначала правый, потом левый, чтобы левый обрабатывался первым
            if (node->right != nullptr) {
                nodeStack.push(node->right);
            }
            if (node->left != nullptr) {
                nodeStack.push(node->left);
            }
        }
        
        return result;
    }
};