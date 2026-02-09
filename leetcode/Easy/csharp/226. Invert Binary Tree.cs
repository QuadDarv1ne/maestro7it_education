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
     * Инвертирует бинарное дерево, меняя местами левые и правые поддеревья для каждого узла.
     * 
     * Алгоритм (рекурсивный):
     * 1. Базовый случай: если узел пустой (null), возвращаем null.
     * 2. Рекурсивно инвертируем левое поддерево.
     * 3. Рекурсивно инвертируем правое поддерево.
     * 4. Меняем местами левый и правый потомков текущего узла.
     * 5. Возвращаем текущий узел.
     * 
     * Сложность:
     * Время: O(n), где n - количество узлов в дереве
     * Пространство: O(h), где h - высота дерева (глубина рекурсии)
     * 
     * @param root Корень бинарного дерева
     * @return Корень инвертированного дерева
     * 
     * Пример:
     * Входное дерево:
     *       4
     *     /   \
     *    2     7
     *   / \   / \
     *  1   3 6   9
     * 
     * Выходное дерево:
     *       4
     *     /   \
     *    7     2
     *   / \   / \
     *  9   6 3   1
     */
    public TreeNode InvertTree(TreeNode root) {
        // Базовый случай: пустой узел
        if (root == null) {
            return null;
        }
        
        // Рекурсивно инвертируем поддеревья
        TreeNode leftInverted = InvertTree(root.left);
        TreeNode rightInverted = InvertTree(root.right);
        
        // Меняем местами потомков
        root.left = rightInverted;
        root.right = leftInverted;
        
        return root;
    }
    
    /**
     * Итеративная версия инвертирования бинарного дерева.
     * 
     * Алгоритм (BFS):
     * 1. Используем очередь для обхода дерева по уровням.
     * 2. Для каждого узла меняем местами его левого и правого потомков.
     * 3. Добавляем потомков в очередь (если они существуют).
     * 
     * Сложность:
     * Время: O(n)
     * Пространство: O(w), где w - максимальная ширина дерева
     * 
     * @param root Корень бинарного дерева
     * @return Корень инвертированного дерева
     */
    public TreeNode InvertTreeIterative(TreeNode root) {
        if (root == null) {
            return null;
        }
        
        Queue<TreeNode> queue = new Queue<TreeNode>();
        queue.Enqueue(root);
        
        while (queue.Count > 0) {
            TreeNode node = queue.Dequeue();
            
            // Меняем местами левого и правого потомков
            TreeNode temp = node.left;
            node.left = node.right;
            node.right = temp;
            
            // Добавляем потомков в очередь, если они существуют
            if (node.left != null) {
                queue.Enqueue(node.left);
            }
            if (node.right != null) {
                queue.Enqueue(node.right);
            }
        }
        
        return root;
    }
}