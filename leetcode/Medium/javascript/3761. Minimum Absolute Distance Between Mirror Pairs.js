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
 * Находит минимальное расстояние между зеркальными парами в массиве.
 * @param {number[]} nums - Исходный массив целых чисел.
 * @return {number} Минимальная разница индексов |i - j| или -1, если пар нет.
 */
var minMirrorPairDistance = function(nums) {
    let minDist = Infinity;
    const lastSeen = new Map();
    
    for (let i = 0; i < nums.length; i++) {
        const val = nums[i];
        
        // 1. Проверка правой части пары
        if (lastSeen.has(val)) {
            const dist = i - lastSeen.get(val);
            if (dist < minDist) {
                minDist = dist;
            }
        }
        
        // 2. Переворот числа и сохранение для будущих пар
        const rev = parseInt(val.toString().split('').reverse().join(''), 10);
        lastSeen.set(rev, i);
    }
    
    return minDist === Infinity ? -1 : minDist;
};