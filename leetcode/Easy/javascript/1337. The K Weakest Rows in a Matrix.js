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
 * Возвращает индексы k самых слабых строк бинарной матрицы.
 *
 * @param {number[][]} mat - матрица m x n из 0 и 1
 * @param {number} k - количество слабейших строк
 * @return {number[]} - индексы строк от самой слабой к более сильной
 */
var kWeakestRows = function(mat, k) {
    const m = mat.length;
    const n = mat[0].length;
    const soldiers = new Array(m);
    
    for (let i = 0; i < m; i++) {
        let left = 0, right = n;
        while (left < right) {
            const mid = Math.floor((left + right) / 2);
            if (mat[i][mid] === 1)
                left = mid + 1;
            else
                right = mid;
        }
        soldiers[i] = left;
    }
    
    // Массив индексов
    const indices = Array.from({length: m}, (_, i) => i);
    indices.sort((a, b) => {
        if (soldiers[a] !== soldiers[b])
            return soldiers[a] - soldiers[b];   // меньше – слабее
        return a - b;                           // при равенстве – по индексу
    });
    
    return indices.slice(0, k);
};