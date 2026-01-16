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
    int maxPathSum(TreeNode* root) {
        /**
         * Находит максимальную сумму пути в бинарном дереве.
         * 
         * Алгоритм:
         * 1. Рекурсивный обход дерева
         * 2. Для каждого узла: max(0, левая ветвь) + max(0, правая ветвь) + значение узла
         * 3. Обновляем глобальный максимум
         * 4. Возвращаем максимальную сумму одной ветви
         * 
         * Сложность: O(n) время, O(h) память
         */
        int maxSum = INT_MIN;
        dfs(root, maxSum);
        return maxSum;
    }
    
private:
    int dfs(TreeNode* node, int& maxSum) {
        if (!node) return 0;
        
        // Рекурсивно вычисляем суммы для левого и правого поддеревьев
        int leftSum = max(0, dfs(node->left, maxSum));
        int rightSum = max(0, dfs(node->right, maxSum));
        
        // Сумма пути через текущий узел
        int pathThroughNode = node->val + leftSum + rightSum;
        
        // Обновляем глобальный максимум
        maxSum = max(maxSum, pathThroughNode);
        
        // Возвращаем максимальную сумму одной ветви
        return node->val + max(leftSum, rightSum);
    }
};