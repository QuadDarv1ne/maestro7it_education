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
 * Подсчитывает количество узлов в полном бинарном дереве.
 * 
 * Алгоритм:
 * 1. Находит высоту дерева по левому и правому краям.
 * 2. Если высоты равны, дерево идеальное (perfect) и количество узлов = 2^h - 1.
 * 3. Если высоты разные, рекурсивно считает для левого и правого поддеревьев.
 * 
 * Сложность:
 * Время: O(log² n), где n - количество узлов
 * Пространство: O(log n) для рекурсивного стека
 * 
 * @param {TreeNode} root - Корень полного бинарного дерева
 * @return {number} Количество узлов в дереве
 * 
 * @example
 * // Вход: [1,2,3,4,5,6]
 * // Выход: 6
 */
var countNodes = function(root) {
    if (!root) {
        return 0;
    }
    
    // Вычисляем высоты по левому и правому краям
    const leftHeight = getHeight(root, true);
    const rightHeight = getHeight(root, false);
    
    // Если дерево идеальное (perfect)
    if (leftHeight === rightHeight) {
        return (1 << leftHeight) - 1;  // 2^h - 1
    }
    
    // Если дерево не идеальное, рекурсивно считаем оба поддерева
    return 1 + countNodes(root.left) + countNodes(root.right);
};

/**
 * Вычисляет высоту дерева, идя только по указанному направлению.
 * 
 * @param {TreeNode} node - Начальный узел
 * @param {boolean} isLeft - true для левого края, false для правого края
 * @return {number} Высота дерева по указанному направлению
 */
function getHeight(node, isLeft) {
    let height = 0;
    while (node) {
        height++;
        node = isLeft ? node.left : node.right;
    }
    return height;
}