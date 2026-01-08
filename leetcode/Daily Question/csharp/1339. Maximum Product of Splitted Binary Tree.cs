/**
 * Максимальное произведение разделенного бинарного дерева
 * 
 * @param root Корень бинарного дерева
 * @return Максимальное произведение сумм двух поддеревьев по модулю 10^9 + 7
 * 
 * Сложность: Время O(n), Память O(h), где n - количество узлов, h - высота дерева
 *
 * Автор: Дуплей Максим Игоревич
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
    private const int MOD = 1000000007;
    private long maxProduct;
    private long totalSum;
    
    // Вычисление общей суммы всех узлов дерева
    private long CalculateTotal(TreeNode node) {
        if (node == null) return 0;
        return node.val + CalculateTotal(node.left) + CalculateTotal(node.right);
    }
    
    // DFS для вычисления сумм поддеревьев и поиска максимального произведения
    private long DFS(TreeNode node) {
        if (node == null) return 0;
        
        // Вычисление суммы текущего поддерева (постфиксный обход)
        long leftSum = DFS(node.left);
        long rightSum = DFS(node.right);
        long subtreeSum = node.val + leftSum + rightSum;
        
        // Если удалить ребро над текущим узлом, получим:
        // - Одно поддерево с суммой = subtreeSum
        // - Другое поддерево с суммой = totalSum - subtreeSum
        long product = subtreeSum * (totalSum - subtreeSum);
        maxProduct = Math.Max(maxProduct, product);
        
        return subtreeSum;
    }
    
    public int MaxProduct(TreeNode root) {
        maxProduct = 0;
        
        // Шаг 1: Вычисление общей суммы
        totalSum = CalculateTotal(root);
        
        // Шаг 2: Поиск максимального произведения
        DFS(root);
        
        return (int)(maxProduct % MOD);
    }
}