/**
 * https://leetcode.com/problems/binary-tree-level-order-traversal/description/
 */

/**
 * Definition for a binary tree node.
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
     * Выполняет обход бинарного дерева по уровням (level-order traversal).
     *
     * Алгоритм:
     * 1. Если корень пуст, возвращаем пустой вектор.
     * 2. Инициализируем очередь, помещаем root.
     * 3. Пока очередь не пуста:
     *    - Получаем размер текущего уровня.
     *    - Для каждого узла уровня: извлекаем его, сохраняем значение,
     *      и добавляем его детей в очередь.
     *    - Добавляем значения уровня в итоговый результат.
     *
     * @param root — корень дерева
     * @return Вектор векторов значений узлов по уровням
     */
    vector<vector<int>> levelOrder(TreeNode* root) {
        if (!root) return {};
        vector<vector<int>> ans;
        queue<TreeNode*> q;
        q.push(root);
        while (!q.empty()) {
            int sz = q.size();
            vector<int> curr;
            for (int i = 0; i < sz; i++) {
                TreeNode* node = q.front(); q.pop();
                curr.push_back(node->val);
                if (node->left) q.push(node->left);
                if (node->right) q.push(node->right);
            }
            ans.push_back(curr);
        }
        return ans;
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