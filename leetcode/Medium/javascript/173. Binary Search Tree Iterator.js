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
 * Итератор для inorder обхода бинарного дерева поиска.
 * 
 * Сложность по времени: O(1) amortized для next(), O(1) для hasNext()
 * Сложность по памяти: O(h), где h - высота дерева
 * 
 * @param {TreeNode} root
 */
var BSTIterator = function(root) {
    this.stack = [];
    this.pushAllLeft(root);
};

/**
 * Добавляет в стек все узлы левой ветки
 * @param {TreeNode} node
 */
BSTIterator.prototype.pushAllLeft = function(node) {
    while (node !== null) {
        this.stack.push(node);
        node = node.left;
    }
};

/**
 * Возвращает следующий наименьший элемент
 * @return {number}
 */
BSTIterator.prototype.next = function() {
    const node = this.stack.pop();
    
    if (node.right !== null) {
        this.pushAllLeft(node.right);
    }
    
    return node.val;
};

/**
 * Проверяет, есть ли следующий элемент
 * @return {boolean}
 */
BSTIterator.prototype.hasNext = function() {
    return this.stack.length > 0;
};