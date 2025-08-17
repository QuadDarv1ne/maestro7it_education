/**
 * https://leetcode.com/problems/maximum-depth-of-binary-tree/description/
 */

/**
 * Определение узла бинарного дерева.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode(int x) { val = x; }
 * }
 */
class Solution {
    /**
     * Задача: Найти максимальную глубину бинарного дерева.
     *
     * Алгоритм:
     * - Если root == null → вернуть 0.
     * - Иначе вернуть 1 + максимум глубин поддеревьев.
     *
     * Сложность:
     * - Время: O(n)
     * - Память: O(h)
     */
    public int maxDepth(TreeNode root) {
        if (root == null) return 0;
        return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
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