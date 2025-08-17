/**
 * https://leetcode.com/problems/maximum-depth-of-binary-tree/description/
 */

/**
 * Определение узла бинарного дерева.
 * public class TreeNode {
 *     public int val;
 *     public TreeNode left;
 *     public TreeNode right;
 *     public TreeNode(int x) { val = x; }
 * }
 */
public class Solution {
    /// <summary>
    /// Задача: Найти максимальную глубину бинарного дерева.
    /// Алгоритм:
    /// - Если узел равен null → вернуть 0.
    /// - Иначе вернуть 1 + максимум глубин левого и правого поддеревьев.
    ///
    /// Сложность:
    /// - Время: O(n), где n — число узлов.
    /// - Память: O(h), где h — высота дерева.
    /// </summary>
    public int MaxDepth(TreeNode root) {
        if (root == null) return 0;
        return 1 + Math.Max(MaxDepth(root.left), MaxDepth(root.right));
    }
}

/*
''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/