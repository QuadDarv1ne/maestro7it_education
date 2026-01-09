/**
 * JavaScript (Рекурсивный DFS)
 * 
 * Находит наименьшее поддерево, содержащее все самые глубокие узлы
 * 
 * @param {TreeNode} root Корень бинарного дерева
 * @return {TreeNode} Корень наименьшего поддерева со всеми самыми глубокими узлами
 * 
 * Сложность: Время O(n), Память O(h), где n - количество узлов, h - высота дерева
 *
 * Автор: Дуплей Максим Игоревич
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
 * @return {TreeNode}
 */
var subtreeWithAllDeepest = function(root) {
    const dfs = (node) => {
        if (!node) return {node: null, depth: 0};
        
        // Рекурсивно обходим левое и правое поддеревья
        const left = dfs(node.left);
        const right = dfs(node.right);
        
        // Сравниваем глубины поддеревьев
        if (left.depth > right.depth) {
            // Самые глубокие узлы в левом поддереве
            return {node: left.node, depth: left.depth + 1};
        } else if (right.depth > left.depth) {
            // Самые глубокие узлы в правом поддереве
            return {node: right.node, depth: right.depth + 1};
        } else {
            // Глубины равны - текущий узел является общим предком
            return {node: node, depth: left.depth + 1};
        }
    };
    
    return dfs(root).node;
};