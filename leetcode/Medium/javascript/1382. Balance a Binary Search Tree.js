/**
 * https://leetcode.com/problems/balance-a-binary-search-tree/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "1382. Balance a Binary Search Tree"
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
 * Балансирует бинарное дерево поиска (BST).
 * 
 * Алгоритм:
 * 1. Выполняет симметричный обход (in-order) BST для получения отсортированного массива значений.
 * 2. Рекурсивно строит сбалансированное BST из отсортированного массива,
 *    выбирая средний элемент в качестве корня для каждого поддерева.
 * 
 * Параметры:
 * root - корень исходного BST
 * 
 * Возвращает:
 * Корень нового сбалансированного BST
 * 
 * Сложность:
 * Время: O(n), где n - количество узлов в дереве
 * Пространство: O(n) для хранения отсортированных значений
 * 
 * @param {TreeNode} root
 * @return {TreeNode}
 */
var balanceBST = function(root) {
    let sortedValues = [];
    
    // Симметричный обход для получения отсортированных значений
    const inorder = (node) => {
        if (!node) return;
        inorder(node.left);
        sortedValues.push(node.val);
        inorder(node.right);
    };
    
    inorder(root);
    
    // Построение сбалансированного BST из отсортированных значений
    const buildBalancedBST = (left, right) => {
        if (left > right) return null;
        
        const mid = Math.floor((left + right) / 2);
        const node = new TreeNode(sortedValues[mid]);
        
        node.left = buildBalancedBST(left, mid - 1);
        node.right = buildBalancedBST(mid + 1, right);
        
        return node;
    };
    
    return buildBalancedBST(0, sortedValues.length - 1);
};