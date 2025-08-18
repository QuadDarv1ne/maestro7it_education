/**
 * https://leetcode.com/problems/balanced-binary-tree/description/
 */

/**
 * Определение узла:
 * function TreeNode(val, left, right) {
 *     this.val = (val===undefined ? 0 : val);
 *     this.left = left === undefined ? null : left;
 *     this.right = right === undefined ? null : right;
 * }
 */

/**
 * Возвращает высоту поддерева или -1 при несбалансированности.
 */
function helper(root) {
    if (!root) return 0;
    const lh = helper(root.left);
    if (lh === -1) return -1;
    const rh = helper(root.right);
    if (rh === -1) return -1;
    if (Math.abs(lh - rh) > 1) return -1;
    return 1 + Math.max(lh, rh);
}

/**
 * Проверка сбалансированности.
 */
var isBalanced = function(root) {
    return helper(root) !== -1;
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