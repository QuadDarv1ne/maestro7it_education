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
    public int MaxPathSum(TreeNode root) {
        /**
         * Находит максимальную сумму пути в бинарном дереве.
         * 
         * Алгоритм:
         * 1. Рекурсивный обход дерева
         * 2. Для каждого узла: Max(0, левая ветвь) + Max(0, правая ветвь) + значение узла
         * 3. Обновляем глобальный максимум
         * 4. Возвращаем максимальную сумму одной ветви
         * 
         * Сложность: O(n) время, O(h) память
         */
        int maxSum = int.MinValue;
        DFS(root, ref maxSum);
        return maxSum;
    }
    
    private int DFS(TreeNode node, ref int maxSum) {
        if (node == null) return 0;
        
        // Рекурсивно вычисляем суммы для левого и правого поддеревьев
        int leftSum = Math.Max(0, DFS(node.left, ref maxSum));
        int rightSum = Math.Max(0, DFS(node.right, ref maxSum));
        
        // Сумма пути через текущий узел
        int pathThroughNode = node.val + leftSum + rightSum;
        
        // Обновляем глобальный максимум
        maxSum = Math.Max(maxSum, pathThroughNode);
        
        // Возвращаем максимальную сумму одной ветви
        return node.val + Math.Max(leftSum, rightSum);
    }
}