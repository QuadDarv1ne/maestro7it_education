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
 * @return {number}
 */
var maxPathSum = function(root) {
    /**
     * Находит максимальную сумму пути в бинарном дереве.
     * 
     * Алгоритм:
     * 1. Рекурсивный обход дерева
     * 2. Для каждого узла: Math.max(0, левая ветвь) + Math.max(0, правая ветвь) + значение узла
     * 3. Обновляем глобальный максимум
     * 4. Возвращаем максимальную сумму одной ветви
     * 
     * Сложность: O(n) время, O(h) память
     */
    let maxSum = -Infinity;
    
    const dfs = (node) => {
        if (!node) return 0;
        
        // Рекурсивно вычисляем суммы для левого и правого поддеревьев
        const leftSum = Math.max(0, dfs(node.left));
        const rightSum = Math.max(0, dfs(node.right));
        
        // Сумма пути через текущий узел
        const pathThroughNode = node.val + leftSum + rightSum;
        
        // Обновляем глобальный максимум
        maxSum = Math.max(maxSum, pathThroughNode);
        
        // Возвращаем максимальную сумму одной ветви
        return node.val + Math.max(leftSum, rightSum);
    };
    
    dfs(root);
    return maxSum;
};