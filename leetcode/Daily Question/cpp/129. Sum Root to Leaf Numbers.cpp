/**
 * Решение задачи LeetCode №129: "Sum Root to Leaf Numbers"
 * Ссылка на задачу: https://leetcode.com/problems/sum-root-to-leaf-numbers/
 * Описание: Дано бинарное дерево, где каждый узел содержит цифру от 0 до 9.
 * Каждое корневое-листовое число образуется путем соединения цифр от корня до листа.
 * Требуется найти сумму всех корневых-листовых чисел.
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
    int sumNumbers(TreeNode* root) {
        /**
         * Вычисляет сумму всех чисел, образованных путями от корня к листьям.
         * 
         * Алгоритм:
         * 1. Рекурсивный обход дерева
         * 2. Накопление значения по пути
         * 3. При достижении листа добавляем к сумме
         * 
         * Сложность: O(n) время, O(h) память
         */
        
        return dfs(root, 0);
    }
    
private:
    int dfs(TreeNode* node, int currentSum) {
        if (!node) {
            return 0;
        }
        
        // Обновляем текущее значение
        currentSum = currentSum * 10 + node->val;
        
        // Если это лист, возвращаем текущее значение
        if (!node->left && !node->right) {
            return currentSum;
        }
        
        // Рекурсивно обходим потомков
        int leftSum = dfs(node->left, currentSum);
        int rightSum = dfs(node->right, currentSum);
        
        return leftSum + rightSum;
    }
};