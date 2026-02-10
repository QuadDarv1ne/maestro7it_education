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
 * Находит длину самого длинного сбалансированного подмассива.
 * Подмассив сбалансирован, если количество уникальных четных чисел
 * равно количеству уникальных нечетных чисел.
 *
 * @param {number[]} nums - Входной массив целых чисел
 * @return {number} Длина самого длинного сбалансированного подмассива
 *
 * @example
 * // Возвращает 4
 * longestBalanced([2, 5, 4, 3])
 * @example
 * // Возвращает 5
 * longestBalanced([3, 2, 2, 5, 4])
 * @example
 * // Возвращает 3
 * longestBalanced([1, 2, 3, 2])
 */
var longestBalanced = function(nums) {
    const n = nums.length;
    let max_len = 0;
    
    for (let i = 0; i < n; i++) {
        const evenSet = new Set();
        const oddSet = new Set();
        
        for (let j = i; j < n; j++) {
            if (nums[j] % 2 === 0) {
                evenSet.add(nums[j]);
            } else {
                oddSet.add(nums[j]);
            }
            
            if (evenSet.size === oddSet.size) {
                max_len = Math.max(max_len, j - i + 1);
            }
        }
    }
    
    return max_len;
};