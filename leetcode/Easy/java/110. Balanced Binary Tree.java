/**
 * https://leetcode.com/problems/balanced-binary-tree/description/
 */

/**
 * Определение узла.
 */
// class TreeNode {
//     int val;
//     TreeNode left, right;
//     TreeNode(int val) { this.val = val; }
// }

class Solution {
    /**
     * Возвращает высоту поддерева или -1, если оно несбалансировано.
     */
    private int height(TreeNode root) {
        if (root == null) return 0;
        int lh = height(root.left);
        if (lh == -1) return -1;
        int rh = height(root.right);
        if (rh == -1) return -1;
        if (Math.abs(lh - rh) > 1) return -1;
        return 1 + Math.max(lh, rh);
    }

    /**
     * Проверяет сбалансированность дерева.
     */
    public boolean isBalanced(TreeNode root) {
        return height(root) != -1;
    }
}

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