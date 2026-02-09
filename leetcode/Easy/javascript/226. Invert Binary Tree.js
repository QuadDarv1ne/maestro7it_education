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
 * Инвертирует бинарное дерево, меняя местами левые и правые поддеревья для каждого узла.
 * 
 * Алгоритм (рекурсивный):
 * 1. Базовый случай: если узел пустой (null), возвращаем null.
 * 2. Рекурсивно инвертируем левое поддерево.
 * 3. Рекурсивно инвертируем правое поддерево.
 * 4. Меняем местами левый и правый потомков текущего узла.
 * 5. Возвращаем текущий узел.
 * 
 * Сложность:
 * Время: O(n), где n - количество узлов в дереве
 * Пространство: O(h), где h - высота дерева (глубина рекурсии)
 * 
 * @param {TreeNode} root - Корень бинарного дерева
 * @return {TreeNode} Корень инвертированного дерева
 * 
 * @example
 * // Входное дерево:
 * //       4
 * //     /   \
 * //    2     7
 * //   / \   / \
 * //  1   3 6   9
 * // 
 * // Выходное дерево:
 * //       4
 * //     /   \
 * //    7     2
 * //   / \   / \
 * //  9   6 3   1
 */
var invertTree = function(root) {
    // Базовый случай: пустой узел
    if (!root) {
        return null;
    }
    
    // Рекурсивно инвертируем поддеревья
    const leftInverted = invertTree(root.left);
    const rightInverted = invertTree(root.right);
    
    // Меняем местами потомков
    root.left = rightInverted;
    root.right = leftInverted;
    
    return root;
};

/**
 * Итеративная версия инвертирования бинарного дерева.
 * 
 * Алгоритм (BFS):
 * 1. Используем очередь для обхода дерева по уровням.
 * 2. Для каждого узла меняем местами его левого и правого потомков.
 * 3. Добавляем потомков в очередь (если они существуют).
 * 
 * Сложность:
 * Время: O(n)
 * Пространство: O(w), где w - максимальная ширина дерева
 * 
 * @param {TreeNode} root - Корень бинарного дерева
 * @return {TreeNode} Корень инвертированного дерева
 */
var invertTreeIterative = function(root) {
    if (!root) {
        return null;
    }
    
    const queue = [root];
    
    while (queue.length > 0) {
        const node = queue.shift();
        
        // Меняем местами левого и правого потомков
        [node.left, node.right] = [node.right, node.left];
        
        // Добавляем потомков в очередь, если они существуют
        if (node.left) {
            queue.push(node.left);
        }
        if (node.right) {
            queue.push(node.right);
        }
    }
    
    return root;
};