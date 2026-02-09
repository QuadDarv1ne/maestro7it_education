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
 *     public TreeNode(int x) { val = x; }
 * }
 */
public class Solution {
    /**
     * Находит наименьшего общего предка двух узлов в бинарном дереве.
     * 
     * Алгоритм (рекурсивный поиск):
     * 1. Если текущий узел равен p или q, возвращаем текущий узел.
     * 2. Рекурсивно ищем p и q в левом и правом поддеревьях.
     * 3. Если оба поддерева вернули не-null узлы, то текущий узел - LCA.
     * 4. Иначе возвращаем то, что не null (или null, если оба null).
     * 
     * Сложность:
     * Время: O(n)
     * Пространство: O(h) - высота дерева
     * 
     * @param root Корень бинарного дерева
     * @param p Первый узел
     * @param q Второй узел
     * @return Наименьший общий предок узлов p и q
     * 
     * Пример:
     * Входное дерево:
     *       3
     *     /   \
     *    5     1
     *   / \   / \
     *  6   2 0   8
     *     / \
     *    7   4
     * 
     * p = 5, q = 1 → LCA = 3
     * p = 5, q = 4 → LCA = 5
     */
    public TreeNode LowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        // Базовый случай: пустой узел или нашли p или q
        if (root == null || root == p || root == q) {
            return root;
        }
        
        // Рекурсивно ищем в левом и правом поддеревьях
        TreeNode left = LowestCommonAncestor(root.left, p, q);
        TreeNode right = LowestCommonAncestor(root.right, p, q);
        
        // Если оба поддерева вернули не-null, текущий узел - LCA
        if (left != null && right != null) {
            return root;
        }
        
        // Иначе возвращаем то, что не null
        return left != null ? left : right;
    }
    
    /**
     * Итеративное решение с использованием стека и родительских указателей.
     * 
     * Алгоритм:
     * 1. Используем стек для обхода дерева.
     * 2. Строим словарь родительских указателей.
     * 3. Находим пути от p и q к корню.
     * 4. Находим пересечение путей.
     * 
     * Сложность:
     * Время: O(n)
     * Пространство: O(n)
     */
    public TreeNode LowestCommonAncestorIterative(TreeNode root, TreeNode p, TreeNode q) {
        if (root == null) return null;
        
        Stack<TreeNode> stack = new Stack<TreeNode>();
        Dictionary<TreeNode, TreeNode> parent = new Dictionary<TreeNode, TreeNode>();
        
        stack.Push(root);
        parent[root] = null;
        
        // Обходим дерево, пока не найдем оба узла
        while (!parent.ContainsKey(p) || !parent.ContainsKey(q)) {
            TreeNode node = stack.Pop();
            
            if (node.left != null) {
                parent[node.left] = node;
                stack.Push(node.left);
            }
            if (node.right != null) {
                parent[node.right] = node;
                stack.Push(node.right);
            }
        }
        
        // Находим всех предков узла p
        HashSet<TreeNode> ancestors = new HashSet<TreeNode>();
        while (p != null) {
            ancestors.Add(p);
            p = parent[p];
        }
        
        // Находим первого общего предка узла q
        while (!ancestors.Contains(q)) {
            q = parent[q];
        }
        
        return q;
    }
}