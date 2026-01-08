/**
 * Максимальная сумма уровня в бинарном дереве
 * 
 * @param {TreeNode} root Корень бинарного дерева
 * @return {number} Наименьший уровень с максимальной суммой значений узлов
 * 
 * Сложность: Время O(n), Память O(w), где n - количество узлов, w - максимальная ширина дерева
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
var maxLevelSum = function(root) {
    if (!root) return 0;
    
    // Инициализация переменных для отслеживания максимума
    let maxSum = -Infinity;
    let maxLevel = 1;
    let currentLevel = 1;
    
    // Очередь для обхода в ширину (BFS)
    const queue = [root];
    
    while (queue.length > 0) {
        let levelSum = 0;
        const levelSize = queue.length;
        
        // Обработка всех узлов текущего уровня
        for (let i = 0; i < levelSize; i++) {
            const node = queue.shift();
            levelSum += node.val;
            
            // Добавление дочерних узлов в очередь
            if (node.left) queue.push(node.left);
            if (node.right) queue.push(node.right);
        }
        
        // Обновление максимума (только если строго больше)
        if (levelSum > maxSum) {
            maxSum = levelSum;
            maxLevel = currentLevel;
        }
        
        currentLevel++;
    }
    
    return maxLevel;
};