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
    /**
     * Подсчитывает количество узлов в полном бинарном дереве.
     * 
     * Алгоритм:
     * 1. Находит высоту дерева по левому и правому краям.
     * 2. Если высоты равны, дерево идеальное (perfect) и количество узлов = 2^h - 1.
     * 3. Если высоты разные, рекурсивно считает для левого и правого поддеревьев.
     * 
     * Сложность:
     * Время: O(log² n), где n - количество узлов
     * Пространство: O(log n) для рекурсивного стека
     * 
     * @param root Корень полного бинарного дерева
     * @return Количество узлов в дереве
     * 
     * Пример:
     * Вход: [1,2,3,4,5,6]
     * Выход: 6
     */
    public int CountNodes(TreeNode root) {
        if (root == null) {
            return 0;
        }
        
        // Вычисляем высоты по левому и правому краям
        int leftHeight = GetHeight(root, true);
        int rightHeight = GetHeight(root, false);
        
        // Если дерево идеальное (perfect)
        if (leftHeight == rightHeight) {
            return (1 << leftHeight) - 1;  // 2^h - 1
        }
        
        // Если дерево не идеальное, рекурсивно считаем оба поддерева
        return 1 + CountNodes(root.left) + CountNodes(root.right);
    }
    
    /**
     * Вычисляет высоту дерева, идя только по указанному направлению.
     * 
     * @param node Начальный узел
     * @param isLeft true для левого края, false для правого края
     * @return Высота дерева по указанному направлению
     */
    private int GetHeight(TreeNode node, bool isLeft) {
        int height = 0;
        while (node != null) {
            height++;
            node = isLeft ? node.left : node.right;
        }
        return height;
    }
}