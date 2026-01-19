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
 * function TreeNode(val, left, right) {
 *     this.val = (val===undefined ? 0 : val)
 *     this.left = (left===undefined ? null : left)
 *     this.right = (right===undefined ? null : right)
 * }
 */
/**
 * @param {TreeNode} root
 * @return {number[]}
 * 
 * @brief Выполняет последующий обход (postorder) бинарного дерева
 */
var postorderTraversal = function(root) {
    const result = [];
    postorderRecursive(root, result);
    return result;
};

/**
 * @brief Рекурсивная вспомогательная функция
 */
function postorderRecursive(node, result) {
    if (node === null) return;
    
    postorderRecursive(node.left, result);  // Обходим левое поддерево
    postorderRecursive(node.right, result); // Обходим правое поддерево
    result.push(node.val);                 // Посещаем корень
}