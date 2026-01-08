/**
 * Максимальное произведение разделенного бинарного дерева
 * 
 * @param {TreeNode} root Корень бинарного дерева
 * @return {number} Максимальное произведение сумм двух поддеревьев по модулю 10^9 + 7
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
 * @return {number}
 */
var maxProduct = function(root) {
    const MOD = 1e9 + 7;
    let maxProduct = 0;
    let totalSum = 0;
    
    // Вычисление общей суммы всех узлов дерева
    const calculateTotal = (node) => {
        if (!node) return 0;
        return node.val + calculateTotal(node.left) + calculateTotal(node.right);
    };
    
    // DFS для вычисления сумм поддеревьев и поиска максимального произведения
    const dfs = (node) => {
        if (!node) return 0;
        
        // Вычисление суммы текущего поддерева (постфиксный обход)
        const leftSum = dfs(node.left);
        const rightSum = dfs(node.right);
        const subtreeSum = node.val + leftSum + rightSum;
        
        // Если удалить ребро над текущим узлом, получим:
        // - Одно поддерево с суммой = subtreeSum
        // - Другое поддерево с суммой = totalSum - subtreeSum
        const product = subtreeSum * (totalSum - subtreeSum);
        maxProduct = Math.max(maxProduct, product);
        
        return subtreeSum;
    };
    
    // Шаг 1: Вычисление общей суммы
    totalSum = calculateTotal(root);
    
    // Шаг 2: Поиск максимального произведения
    dfs(root);
    
    return maxProduct % MOD;
};