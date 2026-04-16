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
 * Находит минимальное кольцевое расстояние до ДРУГОГО равного элемента.
 * @param {number[]} nums
 * @param {number[]} queries
 * @return {number[]}
 */
var solveQueries = function(nums, queries) {
    const n = nums.length;
    const indexMap = new Map();
    
    // 1. Группировка
    for (let i = 0; i < n; i++) {
        const val = nums[i];
        if (!indexMap.has(val)) {
            indexMap.set(val, []);
        }
        indexMap.get(val).push(i);
    }
    
    const answer = [];
    
    // Вспомогательная функция бинарного поиска (возвращает индекс найденного или место вставки)
    const binarySearch = (arr, target) => {
        let low = 0, high = arr.length - 1;
        while (low <= high) {
            const mid = Math.floor((low + high) / 2);
            if (arr[mid] === target) return mid;
            if (arr[mid] < target) low = mid + 1;
            else high = mid - 1;
        }
        return low;
    };
    
    // 2. Обработка запросов
    for (const q of queries) {
        const val = nums[q];
        const pos = indexMap.get(val);
        const m = pos.length;
        
        if (m === 1) {
            answer.push(-1);
            continue;
        }
        
        // Находим позицию q в массиве pos
        const idx = binarySearch(pos, q);
        
        // Соседи (влево и вправо с зацикливанием)
        const leftIdx = (idx - 1 + m) % m;
        const rightIdx = (idx + 1) % m;
        
        const leftPos = pos[leftIdx];
        const rightPos = pos[rightIdx];
        
        const dLeft = Math.abs(q - leftPos);
        const distLeft = Math.min(dLeft, n - dLeft);
        
        const dRight = Math.abs(q - rightPos);
        const distRight = Math.min(dRight, n - dRight);
        
        answer.push(Math.min(distLeft, distRight));
    }
    
    return answer;
};