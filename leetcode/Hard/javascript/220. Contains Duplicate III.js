/**
 * https://leetcode.com/problems/contains-duplicate-iii/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "220. Contains Duplicate III"
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
 * Проверяет, есть ли два элемента с разностью ≤ t на расстоянии ≤ k
 * @param {number[]} nums - Массив чисел
 * @param {number} k - Максимальное расстояние между индексами
 * @param {number} t - Максимальная разность между значениями
 * @return {boolean} - True если существует пара удовлетворяющая условиям
 */
var containsNearbyAlmostDuplicate = function(nums, k, t) {
    if (k < 0 || t < 0) return false;
    
    // Bucket подход
    const bucket = new Map();
    const w = t + 1; // Ширина ведра
    
    for (let i = 0; i < nums.length; i++) {
        const num = nums[i];
        const id = getBucketId(num, w);
        
        // Проверяем текущее ведро
        if (bucket.has(id)) {
            return true;
        }
        
        // Проверяем соседние ведра
        if (bucket.has(id - 1) && Math.abs(num - bucket.get(id - 1)) <= t) {
            return true;
        }
        
        if (bucket.has(id + 1) && Math.abs(num - bucket.get(id + 1)) <= t) {
            return true;
        }
        
        // Добавляем в ведро
        bucket.set(id, num);
        
        // Удаляем элемент, который выходит за пределы окна
        if (i >= k) {
            const oldId = getBucketId(nums[i - k], w);
            bucket.delete(oldId);
        }
    }
    
    return false;
};

/**
 * Вычисляет ID ведра для числа
 * @param {number} num - Число
 * @param {number} w - Ширина ведра
 * @return {number} - ID ведра
 */
function getBucketId(num, w) {
    // Для отрицательных чисел корректируем bucket id
    return num < 0 ? Math.floor((num + 1) / w) - 1 : Math.floor(num / w);
}