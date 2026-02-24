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
    /// Вычисляет сумму всех двоичных чисел от корня до листьев.
    /// </summary>
    /// <param name="root">Корень дерева</param>
    /// <returns>Сумма чисел</returns>
    public int SumRootToLeaf(TreeNode root) {
        return Dfs(root, 0);
    }

    private int Dfs(TreeNode node, int current) {
        if (node == null) return 0;
        current = (current << 1) | node.val; // обновляем число
        if (node.left == null && node.right == null) {
            return current; // лист
        }
        return Dfs(node.left, current) + Dfs(node.right, current);
    }
}