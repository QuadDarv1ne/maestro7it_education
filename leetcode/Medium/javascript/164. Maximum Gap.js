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

var maximumGap = function(nums) {
    /**
     * Находит максимальную разность между последовательными элементами в отсортированной форме.
     * Использует bucket sort для достижения O(n) времени.
     * 
     * Сложность по времени: O(n)
     * Сложность по памяти: O(n)
     */
    const n = nums.length;
    if (n < 2) return 0;
    
    // Находим min и max
    const minVal = Math.min(...nums);
    const maxVal = Math.max(...nums);
    
    if (minVal === maxVal) return 0;
    
    // Размер корзины
    const bucketSize = Math.max(1, Math.floor((maxVal - minVal) / (n - 1)));
    const bucketCount = Math.floor((maxVal - minVal) / bucketSize) + 1;
    
    // Инициализируем корзины [min, max]
    const buckets = Array.from({length: bucketCount}, () => [Infinity, -Infinity]);
    
    // Распределяем элементы по корзинам
    for (const num of nums) {
        const idx = Math.floor((num - minVal) / bucketSize);
        buckets[idx][0] = Math.min(buckets[idx][0], num);
        buckets[idx][1] = Math.max(buckets[idx][1], num);
    }
    
    // Ищем максимальный gap между корзинами
    let maxGap = 0;
    let prevMax = minVal;
    
    for (const [bucketMin, bucketMax] of buckets) {
        if (bucketMin === Infinity) {
            // Пустая корзина
            continue;
        }
        
        maxGap = Math.max(maxGap, bucketMin - prevMax);
        prevMax = bucketMax;
    }
    
    return maxGap;
};