/**
 * Максимальная сумма уровня в бинарном дереве
 * 
 * @param root Корень бинарного дерева
 * @return Наименьший уровень с максимальной суммой значений узлов
 * 
 * Сложность: Время O(n), Память O(w), где n - количество узлов, w - максимальная ширина дерева
 *
 * Автор: Дуплей Максим Игоревич
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
    int maxLevelSum(TreeNode* root) {
        if (!root) return 0;
        
        // Инициализация переменных для отслеживания максимума
        long long maxSum = LLONG_MIN;
        int maxLevel = 1;
        int currentLevel = 1;
        
        // Очередь для обхода в ширину (BFS)
        queue<TreeNode*> q;
        q.push(root);
        
        while (!q.empty()) {
            long long levelSum = 0;
            int levelSize = q.size();
            
            // Обработка всех узлов текущего уровня
            for (int i = 0; i < levelSize; i++) {
                TreeNode* node = q.front();
                q.pop();
                levelSum += node->val;
                
                // Добавление дочерних узлов в очередь
                if (node->left) q.push(node->left);
                if (node->right) q.push(node->right);
            }
            
            // Обновление максимума (только если строго больше)
            if (levelSum > maxSum) {
                maxSum = levelSum;
                maxLevel = currentLevel;
            }
            
            currentLevel++;
        }
        
        return maxLevel;
    }
};