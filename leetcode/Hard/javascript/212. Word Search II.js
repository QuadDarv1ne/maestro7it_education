/**
 * https://leetcode.com/problems/word-search-ii/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "212. Word Search II
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
 * @param {character[][]} board
 * @param {string[]} words
 * @return {string[]}
 */
var findWords = function(board, words) {
    const m = board.length, n = board[0].length;
    const result = [];
    
    // Строим префиксное дерево
    const root = buildTrie(words);
    
    // DFS функция
    function dfs(i, j, node) {
        const ch = board[i][j];
        
        // Если символа нет в дереве
        if (!node.children.has(ch)) {
            return;
        }
        
        const nextNode = node.children.get(ch);
        
        // Если нашли слово
        if (nextNode.word !== null) {
            result.push(nextNode.word);
            nextNode.word = null; // Удаляем слово
        }
        
        // Отмечаем клетку как посещенную
        board[i][j] = '#';
        
        // Проверяем соседние клетки
        if (i > 0) dfs(i - 1, j, nextNode);
        if (j > 0) dfs(i, j - 1, nextNode);
        if (i < m - 1) dfs(i + 1, j, nextNode);
        if (j < n - 1) dfs(i, j + 1, nextNode);
        
        // Возвращаем исходный символ
        board[i][j] = ch;
    }
    
    // Запускаем поиск из каждой клетки
    for (let i = 0; i < m; i++) {
        for (let j = 0; j < n; j++) {
            dfs(i, j, root);
        }
    }
    
    return result;
};

// Класс для узла префиксного дерева
class TrieNode {
    constructor() {
        this.children = new Map();
        this.word = null;
    }
}

// Функция для построения префиксного дерева
function buildTrie(words) {
    const root = new TrieNode();
    
    for (const word of words) {
        let node = root;
        for (const ch of word) {
            if (!node.children.has(ch)) {
                node.children.set(ch, new TrieNode());
            }
            node = node.children.get(ch);
        }
        node.word = word;
    }
    
    return root;
}