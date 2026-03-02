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
 * public class TreeNode {
 *     public int val;
 *     public TreeNode left;
 *     public TreeNode right;
 *     public TreeNode(int val=0, TreeNode left=null, TreeNode right=null) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
public class Solution {
    /// <summary>
    /// Вычисляет сумму значений всех левых листьев в бинарном дереве.
    /// </summary>
    /// <param name="root">Корень дерева.</param>
    /// <returns>Сумма левых листьев.</returns>
    public int SumOfLeftLeaves(TreeNode root) {
        return Dfs(root, false);
    }

    private int Dfs(TreeNode node, bool isLeft) {
        if (node == null) return 0;
        // Если узел - лист и он левый
        if (node.left == null && node.right == null && isLeft) {
            return node.val;
        }
        // Рекурсивно обходим детей
        return Dfs(node.left, true) + Dfs(node.right, false);
    }
}