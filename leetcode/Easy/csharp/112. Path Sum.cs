/**
 * https://leetcode.com/problems/path-sum/description/
 */

/**
 * Определение структуры узла бинарного дерева.
 */
// public class TreeNode {
//     public int val;
//     public TreeNode left;
//     public TreeNode right;
//     public TreeNode(int val=0, TreeNode left=null, TreeNode right=null) {
//         this.val = val;
//         this.left = left;
//         this.right = right;
//     }
// }

public class Solution {
    /// <summary>
    /// Проверяет, существует ли путь от корня до листа, сумма значений которого равна targetSum.
    /// </summary>
    /// <param name="root">Корень бинарного дерева</param>
    /// <param name="targetSum">Целевая сумма</param>
    /// <returns>True, если такой путь существует, иначе False</returns>
    public bool HasPathSum(TreeNode root, int targetSum) {
        if (root == null) return false;
        if (root.left == null && root.right == null) return root.val == targetSum;
        return HasPathSum(root.left, targetSum - root.val) ||
               HasPathSum(root.right, targetSum - root.val);
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