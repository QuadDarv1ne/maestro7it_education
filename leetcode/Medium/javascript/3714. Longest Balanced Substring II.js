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
 * @param {string} s
 * @return {number}
 */
var longestBalanced = function(s) {
    let n = s.length;
    let ans = 0;

    // Случай 1: один символ
    for (let ch of ['a', 'b', 'c']) {
        let cur = 0;
        for (let c of s) {
            if (c === ch) cur++;
            else cur = 0;
            ans = Math.max(ans, cur);
        }
    }

    // Случай 2: два символа
    const pairs = [['a','b'], ['a','c'], ['b','c']];
    for (let [x, y] of pairs) {
        let third = String.fromCharCode('a'.charCodeAt(0) + 'b'.charCodeAt(0) + 'c'.charCodeAt(0) - x.charCodeAt(0) - y.charCodeAt(0));
        let segments = s.split(third);
        for (let seg of segments) {
            let m = seg.length;
            if (m < 2) continue;
            let prefX = new Array(m + 1).fill(0);
            let prefY = new Array(m + 1).fill(0);
            for (let i = 0; i < m; i++) {
                prefX[i + 1] = prefX[i] + (seg[i] === x ? 1 : 0);
                prefY[i + 1] = prefY[i] + (seg[i] === y ? 1 : 0);
            }
            let firstOcc = new Map();
            let diff = 0;
            firstOcc.set(0, 0);
            for (let i = 1; i <= m; i++) {
                if (seg[i - 1] === x) diff++;
                else if (seg[i - 1] === y) diff--;
                if (firstOcc.has(diff)) {
                    let start = firstOcc.get(diff);
                    if (prefX[i] - prefX[start] > 0 && prefY[i] - prefY[start] > 0) {
                        ans = Math.max(ans, i - start);
                    }
                } else {
                    firstOcc.set(diff, i);
                }
            }
        }
    }

    // Случай 3: три символа
    let occ = new Map();
    occ.set('0,0', { idx: -1, ca: 0, cb: 0, cc: 0 });
    let cntA = 0, cntB = 0, cntC = 0;
    for (let i = 0; i < n; i++) {
        if (s[i] === 'a') cntA++;
        else if (s[i] === 'b') cntB++;
        else cntC++;
        let key = `${cntB - cntA},${cntC - cntA}`;
        if (occ.has(key)) {
            let val = occ.get(key);
            if (cntA - val.ca > 0 && cntB - val.cb > 0 && cntC - val.cc > 0) {
                ans = Math.max(ans, i - val.idx);
            }
        } else {
            occ.set(key, { idx: i, ca: cntA, cb: cntB, cc: cntC });
        }
    }

    return ans;
};