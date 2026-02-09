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
     * Возвращает все пути от корня до листьев в бинарном дереве.
     * 
     * Алгоритм (рекурсивный DFS):
     * 1. Если узел пустой, возвращаем пустой вектор.
     * 2. Если узел - лист, добавляем путь к результату.
     * 3. Рекурсивно обходим левое и правое поддеревья.
     * 
     * Сложность:
     * Время: O(n)
     * Пространство: O(h) для рекурсивного стека
     * 
     * @param root Корень бинарного дерева
     * @return Вектор строк, представляющих пути от корня до листьев
     * 
     * Пример:
     * Входное дерево:
     *       1
     *     /   \
     *    2     3
     *     \
     *      5
     * 
     * Выход: ["1->2->5", "1->3"]
     */
    vector<string> binaryTreePaths(TreeNode* root) {
        vector<string> result;
        if (root) {
            dfs(root, "", result);
        }
        return result;
    }
    
private:
    void dfs(TreeNode* node, string path, vector<string>& result) {
        // Добавляем текущий узел к пути
        if (path.empty()) {
            path = to_string(node->val);
        } else {
            path += "->" + to_string(node->val);
        }
        
        // Если узел - лист, добавляем путь к результату
        if (!node->left && !node->right) {
            result.push_back(path);
            return;
        }
        
        // Рекурсивно обходим левое и правое поддеревья
        if (node->left) {
            dfs(node->left, path, result);
        }
        if (node->right) {
            dfs(node->right, path, result);
        }
    }
    
public:
    /**
     * Итеративное решение с использованием стека (DFS).
     * 
     * Алгоритм:
     * 1. Используем стек для хранения пар (узел, путь)
     * 2. При достижении листа добавляем путь к результату
     * 
     * Сложность:
     * Время: O(n)
     * Пространство: O(n) для стека
     */
    vector<string> binaryTreePathsIterative(TreeNode* root) {
        vector<string> result;
        if (!root) return result;
        
        stack<pair<TreeNode*, string>> stk;
        stk.push({root, ""});
        
        while (!stk.empty()) {
            auto [node, path] = stk.top();
            stk.pop();
            
            // Обновляем путь для текущего узла
            string currentPath;
            if (path.empty()) {
                currentPath = to_string(node->val);
            } else {
                currentPath = path + "->" + to_string(node->val);
            }
            
            // Если узел - лист, добавляем путь к результату
            if (!node->left && !node->right) {
                result.push_back(currentPath);
            }
            
            // Добавляем потомков в стек
            if (node->right) {
                stk.push({node->right, currentPath});
            }
            if (node->left) {
                stk.push({node->left, currentPath});
            }
        }
        
        return result;
    }
};