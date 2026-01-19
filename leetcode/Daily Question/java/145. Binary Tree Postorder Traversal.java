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
class Solution {
    /**
     * @brief Выполняет последующий обход (postorder) бинарного дерева
     * 
     * @param root Корень бинарного дерева
     * @return List<Integer> Список значений узлов в порядке postorder
     */
    public List<Integer> postorderTraversal(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        postorderRecursive(root, result);
        return result;
    }
    
    /**
     * @brief Рекурсивная вспомогательная функция
     */
    private void postorderRecursive(TreeNode node, List<Integer> result) {
        if (node == null) return;
        
        postorderRecursive(node.left, result);  // Обходим левое поддерево
        postorderRecursive(node.right, result); // Обходим правое поддерево
        result.add(node.val);                  // Посещаем корень
    }
}