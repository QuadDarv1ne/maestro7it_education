/**
 * Java (Рекурсивный DFS)
 * 
 * Находит наименьшее поддерево, содержащее все самые глубокие узлы
 * 
 * @param root Корень бинарного дерева
 * @return Корень наименьшего поддерева со всеми самыми глубокими узлами
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
    public TreeNode subtreeWithAllDeepest(TreeNode root) {
        return dfs(root).node;
    }
    
    // Вспомогательный класс для возврата узла и глубины
    private class Result {
        TreeNode node;
        int depth;
        Result(TreeNode node, int depth) {
            this.node = node;
            this.depth = depth;
        }
    }
    
    private Result dfs(TreeNode node) {
        if (node == null) return new Result(null, 0);
        
        // Рекурсивно обходим левое и правое поддеревья
        Result left = dfs(node.left);
        Result right = dfs(node.right);
        
        // Сравниваем глубины поддеревьев
        if (left.depth > right.depth) {
            // Самые глубокие узлы в левом поддереве
            return new Result(left.node, left.depth + 1);
        } else if (right.depth > left.depth) {
            // Самые глубокие узлы в правом поддереве
            return new Result(right.node, right.depth + 1);
        } else {
            // Глубины равны - текущий узел является общим предком
            return new Result(node, left.depth + 1);
        }
    }
}