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
 * @return {boolean}
 */
var isTrionic = function(nums) {
    const n = nums.length;
    if (n < 3) return false;
    
    // Вспомогательные функции
    const isIncreasing = (start, end) => {
        for (let i = start; i < end; i++) {
            if (nums[i] >= nums[i + 1]) return false;
        }
        return true;
    };
    
    const isDecreasing = (start, end) => {
        for (let i = start; i < end; i++) {
            if (nums[i] <= nums[i + 1]) return false;
        }
        return true;
    };
    
    // Перебор всех возможных p и q
    for (let p = 1; p < n - 2; p++) {
        for (let q = p + 1; q < n - 1; q++) {
            if (isIncreasing(0, p) && 
                isDecreasing(p, q) && 
                isIncreasing(q, n - 1)) {
                return true;
            }
        }
    }
    
    return false;
};

// TypeScript версия (опционально)
/*
function isTrionic(nums: number[]): boolean {
    // Та же реализация, но с типами
    return isTrionic(nums);
}
*/