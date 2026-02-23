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
 * @param {string[]} cards
 * @param {character} x
 * @return {number}
 */
var score = function(cards, x) {
    const xid = x.charCodeAt(0) - 'a'.charCodeAt(0);
    const cntA = new Array(10).fill(0);
    const cntB = new Array(10).fill(0);
    let cntC = 0;

    for (const card of cards) {
        const a = card.charCodeAt(0) - 'a'.charCodeAt(0);
        const b = card.charCodeAt(1) - 'a'.charCodeAt(0);
        if (a === xid && b === xid) {
            cntC++;
        } else if (a === xid) {
            cntA[b]++;
        } else if (b === xid) {
            cntB[a]++;
        }
    }

    function computeG(cnt) {
        const vals = cnt.filter(v => v > 0).sort((a, b) => b - a);
        vals.push(0);
        const m = vals.length;
        const t = new Array(m).fill(0);
        for (let i = 1; i < m; i++) {
            t[i] = t[i-1] + (vals[i-1] - vals[i]) * i;
        }
        const total = cnt.reduce((s, v) => s + v, 0);
        const g = new Array(total + 1);

        for (let k = 0; k <= total; k++) {
            let i = 0;
            while (i < m - 1 && k >= t[i+1]) i++;
            const groupCnt = i + 1;
            const maxRem = vals[i] - Math.floor((k - t[i]) / groupCnt);
            const rem = total - k;
            const pairs = Math.min(Math.floor(rem / 2), rem - maxRem);
            g[k] = k + pairs;
        }
        return g;
    }

    const gA = computeG(cntA);
    const gB = computeG(cntB);
    const totalA = gA.length - 1;
    const totalB = gB.length - 1;

    let ans = 0;
    for (let cA = 0; cA <= Math.min(cntC, totalA); cA++) {
        const cB = Math.min(cntC - cA, totalB);
        ans = Math.max(ans, gA[cA] + gB[cB]);
    }
    return ans;
};
