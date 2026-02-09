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
 * function TreeNode(val) {
 *     this.val = val;
 *     this.left = this.right = null;
 * }
 */
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
 * @param {TreeNode} root - Корень бинарного дерева
 * @param {TreeNode} p - Первый узел
 * @param {TreeNode} q - Второй узел
 * @return {TreeNode} Наименьший общий предок узлов p и q
 * 
 * @example
 * // Входное дерево:
 * //       3
 * //     /   \
 * //    5     1
 * //   / \   / \
 * //  6   2 0   8
 * //     / \
 * //    7   4
 * // 
 * // p = 5, q = 1 → LCA = 3
 * // p = 5, q = 4 → LCA = 5
 */
var lowestCommonAncestor = function(root, p, q) {
    // Базовый случай: пустой узел или нашли p или q
    if (!root || root === p || root === q) {
        return root;
    }
    
    // Рекурсивно ищем в левом и правом поддеревьях
    const left = lowestCommonAncestor(root.left, p, q);
    const right = lowestCommonAncestor(root.right, p, q);
    
    // Если оба поддерева вернули не-null, текущий узел - LCA
    if (left && right) {
        return root;
    }
    
    // Иначе возвращаем то, что не null
    return left || right;
};

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
var lowestCommonAncestorIterative = function(root, p, q) {
    if (!root) return null;
    
    const stack = [root];
    const parent = new Map();
    
    parent.set(root, null);
    
    // Обходим дерево, пока не найдем оба узла
    while (!parent.has(p) || !parent.has(q)) {
        const node = stack.pop();
        
        if (node.left) {
            parent.set(node.left, node);
            stack.push(node.left);
        }
        if (node.right) {
            parent.set(node.right, node);
            stack.push(node.right);
        }
    }
    
    // Находим всех предков узла p
    const ancestors = new Set();
    while (p) {
        ancestors.add(p);
        p = parent.get(p);
    }
    
    // Находим первого общего предка узла q
    while (!ancestors.has(q)) {
        q = parent.get(q);
    }
    
    return q;
};