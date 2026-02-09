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
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode() {}
 *     TreeNode(int val) { this.val = val; }
 *     TreeNode(int val, TreeNode left, TreeNode right) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {
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
    public TreeNode balanceBST(TreeNode root) {
        List<Integer> sortedValues = new ArrayList<>();
        
        // Симметричный обход для получения отсортированных значений
        inorder(root, sortedValues);
        
        // Построение сбалансированного BST из отсортированных значений
        return buildBalancedBST(sortedValues, 0, sortedValues.size() - 1);
    }
    
    private void inorder(TreeNode node, List<Integer> sortedValues) {
        if (node == null) return;
        inorder(node.left, sortedValues);
        sortedValues.add(node.val);
        inorder(node.right, sortedValues);
    }
    
    private TreeNode buildBalancedBST(List<Integer> sortedValues, int left, int right) {
        if (left > right) return null;
        
        int mid = left + (right - left) / 2;
        TreeNode node = new TreeNode(sortedValues.get(mid));
        
        node.left = buildBalancedBST(sortedValues, left, mid - 1);
        node.right = buildBalancedBST(sortedValues, mid + 1, right);
        
        return node;
    }
}