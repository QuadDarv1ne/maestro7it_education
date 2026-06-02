/**
 * https://leetcode.com/problems/house-robber-ii/description/
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
 * @param {number[]} landStartTime
 * @param {number[]} landDuration
 * @param {number[]} waterStartTime
 * @param {number[]} waterDuration
 * @return {number}
 */
var earliestFinishTime = function(landStartTime, landDuration, waterStartTime, waterDuration) {
    const prepareData = (starts, durs) => {
        const data = [];
        for (let i = 0; i < starts.length; i++) data.push([starts[i], starts[i] + durs[i], durs[i]]);
        data.sort((a, b) => a[0] - b[0]);
        
        const suffix = new Array(data.length).fill(Infinity);
        const prefix = new Array(data.length).fill(Infinity);
        
        if (data.length > 0) {
            suffix[data.length - 1] = data[data.length - 1][1];
            for (let i = data.length - 2; i >= 0; i--) suffix[i] = Math.min(data[i][1], suffix[i + 1]);
            prefix[0] = data[0][2];
            for (let i = 1; i < data.length; i++) prefix[i] = Math.min(data[i][2], prefix[i - 1]);
        }
        return { data, suffix, prefix };
    };
    
    const minEndAfter = (prep, T) => {
        let lo = 0, hi = prep.data.length;
        while (lo < hi) { let mid = Math.floor(lo + (hi - lo) / 2); if (prep.data[mid][0] < T) lo = mid + 1; else hi = mid; }
        return lo === prep.data.length ? Infinity : prep.suffix[lo];
    };
    
    const minDurAtOrBefore = (prep, T) => {
        let lo = 0, hi = prep.data.length;
        while (lo < hi) { let mid = Math.floor(lo + (hi - lo) / 2); if (prep.data[mid][0] <= T) lo = mid + 1; else hi = mid; }
        return lo === 0 ? Infinity : prep.prefix[lo - 1];
    };
    
    const land = prepareData(landStartTime, landDuration);
    const water = prepareData(waterStartTime, waterDuration);
    
    let ans = Infinity;
    
    for (const l of land.data) {
        const eL = l[1];
        const opt1a = minEndAfter(water, eL);
        const opt1bDur = minDurAtOrBefore(water, eL);
        const opt1b = opt1bDur === Infinity ? Infinity : eL + opt1bDur;
        ans = Math.min(ans, opt1a, opt1b);
    }
    
    for (const w of water.data) {
        const eW = w[1];
        const opt2a = minEndAfter(land, eW);
        const opt2bDur = minDurAtOrBefore(land, eW);
        const opt2b = opt2bDur === Infinity ? Infinity : eW + opt2bDur;
        ans = Math.min(ans, opt2a, opt2b);
    }
    
    return ans;
};