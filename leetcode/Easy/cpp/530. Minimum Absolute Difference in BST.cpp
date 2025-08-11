/**
 * https://leetcode.com/problems/minimum-absolute-difference-in-bst/description/?envType=study-plan-v2&envId=top-interview-150
 */

class Solution {
public:
    int getMinimumDifference(TreeNode* root) {
        vector<int> values;
        inorder(root, values);
        int minDiff = INT_MAX;
        for (int i = 1; i < values.size(); ++i) {
            minDiff = min(minDiff, values[i] - values[i-1]);
        }
        return minDiff;
    }

private:
    void inorder(TreeNode* node, vector<int>& values) {
        if (!node) return;
        inorder(node->left, values);
        values.push_back(node->val);
        inorder(node->right, values);
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