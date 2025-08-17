/**
 * https://leetcode.com/problems/symmetric-tree/description/
 */

/**
 * Определение структуры для узла бинарного дерева.
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
     * Проверяет, является ли бинарное дерево зеркально симметричным относительно своего корня.
     *
     * Алгоритм:
     * 1. Симметрия означает, что левое и правое поддерево должны быть зеркальными.
     * 2. Для проверки используем вспомогательную функцию isMirror(t1, t2).
     *    - Если оба узла равны nullptr → это симметрия.
     *    - Если один nullptr, а второй нет → это асимметрия.
     *    - Если значения узлов различаются → это асимметрия.
     *    - Иначе рекурсивно проверяем:
     *         • левый потомок t1 и правый потомок t2
     *         • правый потомок t1 и левый потомок t2
     *
     * Временная сложность: O(n), где n — количество вершин в дереве.
     * Память: O(h), где h — глубина дерева (затраты на рекурсивный стек).
     */
    bool isSymmetric(TreeNode* root) {
        return isMirror(root, root);
    }

private:
    /**
     * Вспомогательная функция для проверки зеркальной симметрии двух поддеревьев.
     */
    bool isMirror(TreeNode* t1, TreeNode* t2) {
        if (!t1 && !t2) return true;
        if (!t1 || !t2) return false;
        if (t1->val != t2->val) return false;

        return isMirror(t1->left, t2->right) && isMirror(t1->right, t2->left);
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