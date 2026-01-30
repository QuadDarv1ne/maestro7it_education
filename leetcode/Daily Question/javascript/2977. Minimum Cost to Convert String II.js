/*
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
 
Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
*/

/**
 * @param {string} source
 * @param {string} target
 * @param {string[]} original
 * @param {string[]} changed
 * @param {number[]} cost
 * @return {number}
 */
var minimumCost = function(source, target, original, changed, cost) {
    class TrieNode {
        constructor() {
            this.children = new Map();
            this.ids = [];
        }
    }
    
    const buildTrie = (strings, strToId) => {
        const root = new TrieNode();
        for (const s of strings) {
            let node = root;
            for (const ch of s) {
                if (!node.children.has(ch)) {
                    node.children.set(ch, new TrieNode());
                }
                node = node.children.get(ch);
            }
            node.ids.push(strToId.get(s));
        }
        return root;
    };
    
    const findMatches = (trie, s, start) => {
        const matches = [];
        let node = trie;
        let pos = start;
        
        while (pos < s.length && node.children.has(s[pos])) {
            node = node.children.get(s[pos]);
            pos++;
            if (node.ids.length > 0) {
                for (const id of node.ids) {
                    matches.push([pos - start, id]);
                }
            }
        }
        return matches;
    };
    
    // Создание уникальных ID для строк
    const unique = new Set([...original, ...changed]);
    const strToId = new Map();
    let idx = 0;
    for (const s of unique) {
        strToId.set(s, idx++);
    }
    
    const n = unique.size;
    const INF = Number.MAX_SAFE_INTEGER;
    
    // Матрица расстояний
    const dist = Array.from({length: n}, () => Array(n).fill(INF));
    for (let i = 0; i < n; i++) {
        dist[i][i] = 0;
    }
    
    for (let i = 0; i < original.length; i++) {
        const sid = strToId.get(original[i]);
        const tid = strToId.get(changed[i]);
        dist[sid][tid] = Math.min(dist[sid][tid], cost[i]);
    }
    
    // Floyd-Warshall
    for (let k = 0; k < n; k++) {
        for (let i = 0; i < n; i++) {
            if (dist[i][k] < INF) {
                for (let j = 0; j < n; j++) {
                    if (dist[k][j] < INF) {
                        dist[i][j] = Math.min(dist[i][j], dist[i][k] + dist[k][j]);
                    }
                }
            }
        }
    }
    
    // Построение Trie
    const srcTrie = buildTrie(unique, strToId);
    const tgtTrie = buildTrie(unique, strToId);
    
    // DP
    const m = source.length;
    const dp = Array(m + 1).fill(INF);
    dp[m] = 0;
    
    for (let i = m - 1; i >= 0; i--) {
        if (source[i] === target[i] && dp[i + 1] < INF) {
            dp[i] = dp[i + 1];
        }
        
        const srcMatches = findMatches(srcTrie, source, i);
        const tgtMatches = findMatches(tgtTrie, target, i);
        
        const tgtByLen = new Map();
        for (const [len, tid] of tgtMatches) {
            if (!tgtByLen.has(len)) {
                tgtByLen.set(len, []);
            }
            tgtByLen.get(len).push(tid);
        }
        
        for (const [srcLen, sid] of srcMatches) {
            if (tgtByLen.has(srcLen) && dp[i + srcLen] < INF) {
                for (const tid of tgtByLen.get(srcLen)) {
                    if (dist[sid][tid] < INF) {
                        dp[i] = Math.min(dp[i], dist[sid][tid] + dp[i + srcLen]);
                    }
                }
            }
        }
    }
    
    return dp[0] < INF ? dp[0] : -1;
};