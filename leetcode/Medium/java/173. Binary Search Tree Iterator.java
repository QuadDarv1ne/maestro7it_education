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
class BSTIterator {
    private Stack<TreeNode> stack;
    
    /**
     * Итератор для inorder обхода бинарного дерева поиска.
     * 
     * Сложность по времени: O(1) amortized для next(), O(1) для hasNext()
     * Сложность по памяти: O(h), где h - высота дерева
     */
    public BSTIterator(TreeNode root) {
        stack = new Stack<>();
        pushAllLeft(root);
    }
    
    /**
     * Добавляет в стек все узлы левой ветки
     */
    private void pushAllLeft(TreeNode node) {
        while (node != null) {
            stack.push(node);
            node = node.left;
        }
    }
    
    /**
     * Возвращает следующий наименьший элемент
     */
    public int next() {
        TreeNode node = stack.pop();
        
        if (node.right != null) {
            pushAllLeft(node.right);
        }
        
        return node.val;
    }
    
    /**
     * Проверяет, есть ли следующий элемент
     */
    public boolean hasNext() {
        return !stack.isEmpty();
    }
}