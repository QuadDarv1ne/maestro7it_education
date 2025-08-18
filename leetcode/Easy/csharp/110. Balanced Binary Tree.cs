/**
 * https://leetcode.com/problems/balanced-binary-tree/description/
 */

// public class TreeNode {
//     public int val;
//     public TreeNode left, right;
//     public TreeNode(int val=0, TreeNode left=null, TreeNode right=null) {
//         this.val = val;
//         this.left = left;
//         this.right = right;
//     }
// }

public class Solution {
    /// <summary>
    /// Возвращает высоту дерева, или -1, если дерево несбалансировано.
    /// </summary>
    private int Height(TreeNode root) {
        if (root == null) return 0;
        int lh = Height(root.left);
        if (lh == -1) return -1;
        int rh = Height(root.right);
        if (rh == -1) return -1;
        if (Math.Abs(lh - rh) > 1) return -1;
        return 1 + Math.Max(lh, rh);
    }

    /// <summary>
    /// Проверяет, является ли дерево сбалансированным.
    /// </summary>
    public bool IsBalanced(TreeNode root) {
        return Height(root) != -1;
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