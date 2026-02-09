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
    public List<String> binaryTreePaths(TreeNode root) {
        List<String> result = new ArrayList<>();
        if (root != null) {
            dfs(root, "", result);
        }
        return result;
    }
    
    private void dfs(TreeNode node, String path, List<String> result) {
        // Добавляем текущий узел к пути
        StringBuilder currentPath = new StringBuilder(path);
        if (currentPath.length() == 0) {
            currentPath.append(node.val);
        } else {
            currentPath.append("->").append(node.val);
        }
        
        // Если узел - лист, добавляем путь к результату
        if (node.left == null && node.right == null) {
            result.add(currentPath.toString());
            return;
        }
        
        // Рекурсивно обходим левое и правое поддеревья
        if (node.left != null) {
            dfs(node.left, currentPath.toString(), result);
        }
        if (node.right != null) {
            dfs(node.right, currentPath.toString(), result);
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
    public List<String> binaryTreePathsIterative(TreeNode root) {
        List<String> result = new ArrayList<>();
        if (root == null) return result;
        
        Deque<Pair<TreeNode, String>> stack = new ArrayDeque<>();
        stack.push(new Pair<>(root, ""));
        
        while (!stack.isEmpty()) {
            Pair<TreeNode, String> pair = stack.pop();
            TreeNode node = pair.getKey();
            String path = pair.getValue();
            
            // Обновляем путь для текущего узла
            StringBuilder currentPath = new StringBuilder(path);
            if (currentPath.length() == 0) {
                currentPath.append(node.val);
            } else {
                currentPath.append("->").append(node.val);
            }
            
            // Если узел - лист, добавляем путь к результату
            if (node.left == null && node.right == null) {
                result.add(currentPath.toString());
            }
            
            // Добавляем потомков в стек
            if (node.right != null) {
                stack.push(new Pair<>(node.right, currentPath.toString()));
            }
            if (node.left != null) {
                stack.push(new Pair<>(node.left, currentPath.toString()));
            }
        }
        
        return result;
    }
    
    // Вспомогательный класс Pair (для Java версий без стандартного Pair)
    private static class Pair<K, V> {
        private K key;
        private V value;
        
        public Pair(K key, V value) {
            this.key = key;
            this.value = value;
        }
        
        public K getKey() { return key; }
        public V getValue() { return value; }
    }
}