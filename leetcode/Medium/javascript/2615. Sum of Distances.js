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
 * @param {number[]} nums
 * @return {number[]}
 */
var distance = function(nums) {
    const n = nums.length;
    const map = new Map();
    
    for (let i = 0; i < n; i++) {
        if (!map.has(nums[i])) map.set(nums[i], []);
        map.get(nums[i]).push(i);
    }
    
    const ans = new Array(n).fill(0);
    
    for (const indices of map.values()) {
        const m = indices.length;
        const prefix = new Array(m + 1).fill(0);
        for (let i = 0; i < m; i++) {
            prefix[i + 1] = prefix[i] + indices[i];
        }
        
        for (let i = 0; i < m; i++) {
            const idx = indices[i];
            const leftCount = i;
            const leftSum = prefix[i];
            const leftDist = idx * leftCount - leftSum;
            
            const rightCount = m - i - 1;
            const rightSum = prefix[m] - prefix[i + 1];
            const rightDist = rightSum - idx * rightCount;
            
            ans[idx] = leftDist + rightDist;
        }
    }
    return ans;
};