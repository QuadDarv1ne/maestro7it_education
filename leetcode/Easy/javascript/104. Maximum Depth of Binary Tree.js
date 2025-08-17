/**
 * https://leetcode.com/problems/maximum-depth-of-binary-tree/description/
 */

/**
 * Определение узла бинарного дерева.
 * function TreeNode(val, left, right) {
 *     this.val = (val===undefined ? 0 : val);
 *     this.left = (left===undefined ? null : left);
 *     this.right = (right===undefined ? null : right);
 * }
 */

/**
 * Задача: Найти максимальную глубину бинарного дерева.
 *
 * Алгоритм:
 * - Если root == null → вернуть 0.
 * - Иначе 1 + максимум глубин поддеревьев.
 *
 * Сложность:
 * - Время: O(n), где n — число узлов.
 * - Память: O(h), где h — высота дерева.
 *
 * @param {TreeNode} root
 * @return {number}
 */
var maxDepth = function(root) {
    if (root == null) return 0;
    return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
};

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