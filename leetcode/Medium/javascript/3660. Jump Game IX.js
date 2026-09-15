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
 * Для каждого индекса i вычисляет максимальное значение в nums, 
 * которое может быть достигнуто, начиная с i, следуя правилам прыжков.
 * @param {number[]} nums
 * @return {number[]}
 */
var maxValue = function(nums) {
    const n = nums.length;
    const ans = new Array(n);

    const prefixMax = new Array(n);
    let curMax = nums[0];
    for (let i = 0; i < n; i++) {
        curMax = Math.max(curMax, nums[i]);
        prefixMax[i] = curMax;
    }

    const suffixMin = new Array(n);
    let curMin = nums[n - 1];
    for (let i = n - 1; i >= 0; i--) {
        curMin = Math.min(curMin, nums[i]);
        suffixMin[i] = curMin;
    }

    const cutIndices = [];
    for (let i = 0; i < n - 1; i++) {
        if (prefixMax[i] <= suffixMin[i + 1]) {
            cutIndices.push(i);
        }
    }

    let start = 0;
    for (const cut of cutIndices) {
        const end = cut;
        const segMax = Math.max(...nums.slice(start, end + 1));
        for (let i = start; i <= end; i++) {
            ans[i] = segMax;
        }
        start = end + 1;
    }

    if (start < n) {
        const lastSegMax = Math.max(...nums.slice(start));
        for (let i = start; i < n; i++) {
            ans[i] = lastSegMax;
        }
    }

    return ans;
};