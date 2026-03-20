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
 * @param {number[][]} grid
 * @param {number} k
 * @return {number[][]}
 */
var minAbsDiff = function(grid, k) {
    const m = grid.length;
    const n = grid[0].length;
    const rows = m - k + 1;
    const cols = n - k + 1;
    
    // Создаем двумерный массив результата
    const result = Array.from({ length: rows }, () => Array(cols).fill(0));
    
    for (let i = 0; i < rows; i++) {
        for (let j = 0; j < cols; j++) {
            // Используем Set для уникальных значений
            const uniqueSet = new Set();
            
            for (let x = i; x < i + k; x++) {
                for (let y = j; y < j + k; y++) {
                    uniqueSet.add(grid[x][y]);
                }
            }
            
            // Преобразуем Set в массив
            const uniqueVals = Array.from(uniqueSet);
            
            // Если все значения одинаковы
            if (uniqueVals.length === 1) {
                result[i][j] = 0;
                continue;
            }
            
            // Сортируем числовые значения
            uniqueVals.sort((a, b) => a - b);
            
            // Ищем минимальную разность
            let minDiff = Infinity;
            for (let idx = 1; idx < uniqueVals.length; idx++) {
                const diff = uniqueVals[idx] - uniqueVals[idx - 1];
                if (diff < minDiff) {
                    minDiff = diff;
                }
            }
            
            result[i][j] = minDiff;
        }
    }
    
    return result;
};