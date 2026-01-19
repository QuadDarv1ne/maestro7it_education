/*
LeetCode 140: Word Break II

Задача: Дана строка s и словарь строк wordDict. Добавьте пробелы в s, чтобы
построить предложение, где каждое слово является допустимым словом из словаря.
Верните все такие возможные предложения в любом порядке.

Примечание: Одно и то же слово из словаря может быть использовано несколько раз.

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Полезные ссылки:
1. ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1: @quadd4rv1n7
3. Telegram №2: @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
*/

// Узел Trie
class TrieNode {
    constructor() {
        this.children = new Map();
        this.isEnd = false;
    }
}

// Префиксное дерево
class Trie {
    constructor() {
        this.root = new TrieNode();
    }
    
    // Вставка слова в Trie
    insert(word) {
        let node = this.root;
        for (const char of word) {
            if (!node.children.has(char)) {
                node.children.set(char, new TrieNode());
            }
            node = node.children.get(char);
        }
        node.isEnd = true;
    }
    
    // Проверка существования слова
    search(word) {
        let node = this.root;
        for (const char of word) {
            if (!node.children.has(char)) {
                return false;
            }
            node = node.children.get(char);
        }
        return node.isEnd;
    }
}

/**
 * Подход 1: DFS с мемоизацией и Trie (Наиболее оптимальный)
 * Время: O(n * 2^n) в худшем случае, Память: O(n * 2^n)
 * 
 * Используем Trie для эффективного поиска слов и DFS с мемоизацией
 * для построения всех возможных предложений.
 * 
 * @param {string} s
 * @param {string[]} wordDict
 * @return {string[]}
 */
var wordBreak = function(s, wordDict) {
    // Строим Trie из словаря
    const trie = new Trie();
    for (const word of wordDict) {
        trie.insert(word);
    }
    
    // Map для мемоизации
    const memo = new Map();
    
    function dfs(start) {
        // Если достигли конца строки
        if (start === s.length) {
            return [""];
        }
        
        // Если результат уже вычислен
        if (memo.has(start)) {
            return memo.get(start);
        }
        
        const results = [];
        
        // Пробуем все возможные слова
        for (let end = start + 1; end <= s.length; end++) {
            const word = s.substring(start, end);
            
            if (trie.search(word)) {
                const subResults = dfs(end);
                
                for (const sub of subResults) {
                    if (sub === "") {
                        results.push(word);
                    } else {
                        results.push(word + " " + sub);
                    }
                }
            }
        }
        
        memo.set(start, results);
        return results;
    }
    
    return dfs(0);
};

/**
 * Подход 2: DFS с мемоизацией (без Trie)
 * Время: O(n * 2^n), Память: O(n * 2^n)
 * 
 * Простой подход с использованием Set для словаря.
 * 
 * @param {string} s
 * @param {string[]} wordDict
 * @return {string[]}
 */
var wordBreakSimple = function(s, wordDict) {
    const wordSet = new Set(wordDict);
    const memo = new Map();
    
    function dfs(start) {
        if (start === s.length) {
            return [""];
        }
        
        if (memo.has(start)) {
            return memo.get(start);
        }
        
        const results = [];
        
        for (let end = start + 1; end <= s.length; end++) {
            const word = s.substring(start, end);
            
            if (wordSet.has(word)) {
                const subResults = dfs(end);
                
                for (const sub of subResults) {
                    if (sub === "") {
                        results.push(word);
                    } else {
                        results.push(word + " " + sub);
                    }
                }
            }
        }
        
        memo.set(start, results);
        return results;
    }
    
    return dfs(0);
};

/**
 * Подход 3: Динамическое программирование
 * Время: O(n^2 * m), где m - количество слов, Память: O(n^2)
 * 
 * @param {string} s
 * @param {string[]} wordDict
 * @return {string[]}
 */
var wordBreakDP = function(s, wordDict) {
    const wordSet = new Set(wordDict);
    const n = s.length;
    
    // dp[i] - список всех возможных предложений для s[0:i]
    const dp = Array(n + 1).fill(null).map(() => []);
    dp[0] = [""];
    
    for (let i = 1; i <= n; i++) {
        for (let j = 0; j < i; j++) {
            const word = s.substring(j, i);
            
            if (wordSet.has(word) && dp[j].length > 0) {
                for (const sentence of dp[j]) {
                    if (sentence === "") {
                        dp[i].push(word);
                    } else {
                        dp[i].push(sentence + " " + word);
                    }
                }
            }
        }
    }
    
    return dp[n];
};