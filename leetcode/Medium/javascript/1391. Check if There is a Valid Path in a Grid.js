/**
 * https://leetcode.com/problems/balance-a-binary-search-tree/description/
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
 * @return {boolean}
 */
var hasValidPath = function(grid) {
    const m = grid.length, n = grid[0].length;
    // delta для направлений 0: вверх, 1: вправо, 2: вниз, 3: влево
    const dirs = [[-1, 0], [0, 1], [1, 0], [0, -1]];
    
    // Предрасчёт допустимых направлений для каждого типа труб (1-6)
    const pipes = [
        [],          // индекс 0 не используется
        [1, 3],      // тип 1
        [0, 2],      // тип 2
        [2, 3],      // тип 3
        [1, 2],      // тип 4
        [0, 3],      // тип 5
        [0, 1]       // тип 6
    ];
    
    const visited = Array.from({ length: m }, () => new Array(n).fill(false));
    const queue = [[0, 0]];
    visited[0][0] = true;
    
    while (queue.length) {
        const [x, y] = queue.shift();
        if (x === m-1 && y === n-1) return true;
        
        const type = grid[x][y];
        for (const d of pipes[type]) {
            const nx = x + dirs[d][0];
            const ny = y + dirs[d][1];
            if (nx < 0 || nx >= m || ny < 0 || ny >= n || visited[nx][ny]) continue;
            
            const nextType = grid[nx][ny];
            // Проверка возможности обратного движения
            for (const backDir of pipes[nextType]) {
                if (backDir === (d ^ 2)) {
                    visited[nx][ny] = true;
                    queue.push([nx, ny]);
                    break;
                }
            }
        }
    }
    return false;
};