/**
 * JavaScript (Binary Search + BFS)
 * 
 * Последний день, когда можно перейти от верхней строки к нижней
 * 
 * @param {number} row Количество строк в сетке
 * @param {number} col Количество столбцов в сетке  
 * @param {number[][]} cells Массив ячеек, которые становятся водой каждый день
 * @return {number} Последний день (0-индексированный), когда можно перейти сверху вниз
 * 
 * Сложность: Время O((row*col) * log(row*col)), Память O(row*col)
 *
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
 * @param {number} row
 * @param {number} col
 * @param {number[][]} cells
 * @return {number}
 */
var latestDayToCross = function(row, col, cells) {
    const canCross = (day) => {
        const grid = Array.from({length: row}, () => new Array(col).fill(0));
        
        for (let i = 0; i < day; i++) {
            const [r, c] = cells[i];
            grid[r-1][c-1] = 1;
        }
        
        const queue = [];
        for (let c = 0; c < col; c++) {
            if (grid[0][c] === 0) {
                queue.push([0, c]);
                grid[0][c] = 1;
            }
        }
        
        const directions = [[-1, 0], [1, 0], [0, -1], [0, 1]];
        
        for (let i = 0; i < queue.length; i++) {
            const [r, c] = queue[i];
            
            if (r === row - 1) return true;
            
            for (const [dr, dc] of directions) {
                const nr = r + dr;
                const nc = c + dc;
                
                if (nr >= 0 && nr < row && nc >= 0 && nc < col && grid[nr][nc] === 0) {
                    grid[nr][nc] = 1;
                    queue.push([nr, nc]);
                }
            }
        }
        
        return false;
    };
    
    let left = 0, right = cells.length;
    
    while (left < right) {
        const mid = Math.floor(left + (right - left + 1) / 2);
        if (canCross(mid)) {
            left = mid;
        } else {
            right = mid - 1;
        }
    }
    
    return left;
};