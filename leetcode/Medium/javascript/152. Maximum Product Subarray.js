/**
 * https://leetcode.com/problems/maximum-product-subarray/description/
 * Автор: Дуплей Максим Игоревич
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
 * Находит максимальное произведение подмассива.
 * 
 * @param {number[]} nums - Массив целых чисел
 * @return {number} Максимальное произведение подмассива
 * 
 * Алгоритм:
 * - Отслеживаем максимальное и минимальное произведение
 * - При встрече отрицательного числа меняем их местами
 * - На каждом шаге обновляем результат
 */
var maxProduct = function(nums) {
    if (!nums || nums.length === 0) {
        return 0;
    }
    
    let maxProd = nums[0];
    let minProd = nums[0];
    let result = nums[0];
    
    for (let i = 1; i < nums.length; i++) {
        const current = nums[i];
        
        // Если число отрицательное, меняем местами max и min
        if (current < 0) {
            [maxProd, minProd] = [minProd, maxProd];
        }
        
        // Обновляем максимальное и минимальное произведение
        maxProd = Math.max(current, maxProd * current);
        minProd = Math.min(current, minProd * current);
        
        // Обновляем результат
        result = Math.max(result, maxProd);
    }
    
    return result;
};