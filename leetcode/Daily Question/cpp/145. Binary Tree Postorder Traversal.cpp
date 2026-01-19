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
     * @brief Выполняет последующий обход (postorder) бинарного дерева
     * 
     * Последующий обход (postorder traversal):
     * 1. Обходим левое поддерево
     * 2. Обходим правое поддерево
     * 3. Посещаем корень
     * 
     * Рекурсивный подход:
     * - Простая реализация, но может вызвать переполнение стека для больших деревьев
     * 
     * @param root Корень бинарного дерева
     * @return vector<int> Вектор значений узлов в порядке postorder
     */
    vector<int> postorderTraversal(TreeNode* root) {
        vector<int> result;
        postorderRecursive(root, result);
        return result;
    }
    
private:
    /**
     * @brief Рекурсивная вспомогательная функция для последующего обхода
     * 
     * @param node Текущий узел
     * @param result Вектор для хранения результата
     */
    void postorderRecursive(TreeNode* node, vector<int>& result) {
        if (node == nullptr) return;
        
        postorderRecursive(node->left, result);  // Обходим левое поддерево
        postorderRecursive(node->right, result); // Обходим правое поддерево
        result.push_back(node->val);            // Посещаем корень
    }
};