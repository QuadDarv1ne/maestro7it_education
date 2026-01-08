/**
 * Максимальная сумма уровня в бинарном дереве
 * 
 * @param root Корень бинарного дерева
 * @return Наименьший уровень с максимальной суммой значений узлов
 * 
 * Сложность: Время O(n), Память O(w), где n - количество узлов, w - максимальная ширина дерева
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
    public int MaxLevelSum(TreeNode root) {
        if (root == null) return 0;
        
        // Инициализация переменных для отслеживания максимума
        long maxSum = long.MinValue;
        int maxLevel = 1;
        int currentLevel = 1;
        
        // Очередь для обхода в ширину (BFS)
        Queue<TreeNode> queue = new Queue<TreeNode>();
        queue.Enqueue(root);
        
        while (queue.Count > 0) {
            long levelSum = 0;
            int levelSize = queue.Count;
            
            // Обработка всех узлов текущего уровня
            for (int i = 0; i < levelSize; i++) {
                TreeNode node = queue.Dequeue();
                levelSum += node.val;
                
                // Добавление дочерних узлов в очередь
                if (node.left != null) queue.Enqueue(node.left);
                if (node.right != null) queue.Enqueue(node.right);
            }
            
            // Обновление максимума (только если строго больше)
            if (levelSum > maxSum) {
                maxSum = levelSum;
                maxLevel = currentLevel;
            }
            
            currentLevel++;
        }
        
        return maxLevel;
    }
}