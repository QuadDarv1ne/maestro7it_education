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
 * @param {number[]} parent
 * @param {string} s
 * @return {number}
 */
var countPalindromePaths = function(parent, s) {
    const n = parent.length;
    const tree = Array.from({ length: n }, () => []);
    for (let i = 1; i < n; i++) {
        tree[parent[i]].push(i);
    }
    
    let ans = 0;
    const maskCount = new Map();
    
    const dfs = (node, mask) => {
        ans += maskCount.get(mask) || 0;
        for (let i = 0; i < 26; i++) {
            ans += maskCount.get(mask ^ (1 << i)) || 0;
        }
        
        maskCount.set(mask, (maskCount.get(mask) || 0) + 1);
        
        for (const child of tree[node]) {
            const childMask = mask ^ (1 << (s.charCodeAt(child) - 97));
            dfs(child, childMask);
        }
    };
    
    dfs(0, 0);
    return ans;
};