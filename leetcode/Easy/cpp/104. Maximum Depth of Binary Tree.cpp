/**
 * https://leetcode.com/problems/maximum-depth-of-binary-tree/description/
 */

/**
 * Определение структуры узла бинарного дерева.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 * };
 */

class Solution {
public:
    /**
     * Задача: Найти максимальную глубину бинарного дерева.
     *
     * Алгоритм:
     * - Если узел равен nullptr → вернуть 0.
     * - Иначе вернуть 1 + максимум глубин левого и правого поддеревьев.
     *
     * Сложность:
     * - Время: O(n), где n — число узлов.
     * - Память: O(h), где h — высота дерева.
     */
    int maxDepth(TreeNode* root) {
        if (root == nullptr) return 0;
        return 1 + max(maxDepth(root->left), maxDepth(root->right));
    }
};

/*
''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/