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
     * Возвращает все пути от корня до листьев в бинарном дереве.
     * 
     * Алгоритм (рекурсивный DFS):
     * 1. Если узел пустой, возвращаем пустой список.
     * 2. Если узел - лист, добавляем путь к результату.
     * 3. Рекурсивно обходим левое и правое поддеревья.
     * 
     * Сложность:
     * Время: O(n)
     * Пространство: O(h) для рекурсивного стека
     * 
     * @param root Корень бинарного дерева
     * @return Список строк, представляющих пути от корня до листьев
     * 
     * Пример:
     * Входное дерево:
     *       1
     *     /   \
     *    2     3
     *     \
     *      5
     * 
     * Выход: ["1->2->5", "1->3"]
     */
    public IList<string> BinaryTreePaths(TreeNode root) {
        var result = new List<string>();
        if (root != null) {
            Dfs(root, "", result);
        }
        return result;
    }
    
    private void Dfs(TreeNode node, string path, List<string> result) {
        // Добавляем текущий узел к пути
        string currentPath;
        if (string.IsNullOrEmpty(path)) {
            currentPath = node.val.ToString();
        } else {
            currentPath = path + "->" + node.val;
        }
        
        // Если узел - лист, добавляем путь к результату
        if (node.left == null && node.right == null) {
            result.Add(currentPath);
            return;
        }
        
        // Рекурсивно обходим левое и правое поддеревья
        if (node.left != null) {
            Dfs(node.left, currentPath, result);
        }
        if (node.right != null) {
            Dfs(node.right, currentPath, result);
        }
    }
    
    /**
     * Итеративное решение с использованием стека (DFS).
     * 
     * Алгоритм:
     * 1. Используем стек для хранения пар (узел, путь)
     * 2. При достижении листа добавляем путь к результату
     * 
     * Сложность:
     * Время: O(n)
     * Пространство: O(n) для стека
     */
    public IList<string> BinaryTreePathsIterative(TreeNode root) {
        var result = new List<string>();
        if (root == null) return result;
        
        var stack = new Stack<(TreeNode, string)>();
        stack.Push((root, ""));
        
        while (stack.Count > 0) {
            var (node, path) = stack.Pop();
            
            // Обновляем путь для текущего узла
            string currentPath;
            if (string.IsNullOrEmpty(path)) {
                currentPath = node.val.ToString();
            } else {
                currentPath = path + "->" + node.val;
            }
            
            // Если узел - лист, добавляем путь к результату
            if (node.left == null && node.right == null) {
                result.Add(currentPath);
            }
            
            // Добавляем потомков в стек
            if (node.right != null) {
                stack.Push((node.right, currentPath));
            }
            if (node.left != null) {
                stack.Push((node.left, currentPath));
            }
        }
        
        return result;
    }
}