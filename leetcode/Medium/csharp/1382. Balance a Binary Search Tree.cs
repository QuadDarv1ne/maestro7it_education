/**
 * https://leetcode.com/problems/balance-a-binary-search-tree/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "1382. Balance a Binary Search Tree"
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
    /**
     * Балансирует бинарное дерево поиска (BST).
     * 
     * Алгоритм:
     * 1. Выполняет симметричный обход (in-order) BST для получения отсортированного списка значений.
     * 2. Рекурсивно строит сбалансированное BST из отсортированного списка,
     *    выбирая средний элемент в качестве корня для каждого поддерева.
     * 
     * Параметры:
     * root - корень исходного BST
     * 
     * Возвращает:
     * Корень нового сбалансированного BST
     * 
     * Сложность:
     * Время: O(n), где n - количество узлов в дереве
     * Пространство: O(n) для хранения отсортированных значений
     */
    public TreeNode BalanceBST(TreeNode root) {
        List<int> sortedValues = new List<int>();
        
        // Симметричный обход для получения отсортированных значений
        void Inorder(TreeNode node) {
            if (node == null) return;
            Inorder(node.left);
            sortedValues.Add(node.val);
            Inorder(node.right);
        }
        
        Inorder(root);
        
        // Построение сбалансированного BST из отсортированных значений
        TreeNode BuildBalancedBST(int left, int right) {
            if (left > right) return null;
            
            int mid = left + (right - left) / 2;
            TreeNode node = new TreeNode(sortedValues[mid]);
            
            node.left = BuildBalancedBST(left, mid - 1);
            node.right = BuildBalancedBST(mid + 1, right);
            
            return node;
        }
        
        return BuildBalancedBST(0, sortedValues.Count - 1);
    }
}