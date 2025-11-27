/*
 * https://leetcode.com/problems/maximum-subarray-sum-with-length-divisible-by-k/description/?envType=daily-question&envId=2025-11-27
 * Автор: Дуплей Максим Игоревич
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 */

var maxSubarraySum = function(nums, k) {
    const n = nums.length;
    const prefix = new Array(n + 1).fill(0);
    
    for (let i = 0; i < n; i++) {
        prefix[i + 1] = prefix[i] + nums[i];
    }
    
    let maxSum = -Infinity;
    const minPrefix = new Map();
    minPrefix.set(0, 0);
    
    for (let i = 1; i <= n; i++) {
        const remainder = i % k;
        
        if (minPrefix.has(remainder)) {
            const currentSum = prefix[i] - minPrefix.get(remainder);
            maxSum = Math.max(maxSum, currentSum);
        }
        
        if (!minPrefix.has(remainder)) {
            minPrefix.set(remainder, prefix[i]);
        } else {
            minPrefix.set(remainder, Math.min(minPrefix.get(remainder), prefix[i]));
        }
    }
    
    return maxSum === -Infinity ? 0 : maxSum;
};

/*
 * Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
*/