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
 * @param {character[][]} grid
 * @return {boolean}
 */
var containsCycle = function(grid) {
    const m = grid.length, n = grid[0].length;
    const visited = Array.from({ length: m }, () => Array(n).fill(false));
    const dir = [[0, 1], [1, 0], [0, -1], [-1, 0]];
    
    const dfs = (x, y, px, py) => {
        visited[x][y] = true;
        for (const [dx, dy] of dir) {
            const nx = x + dx, ny = y + dy;
            if (nx < 0 || nx >= m || ny < 0 || ny >= n || grid[nx][ny] !== grid[x][y]) 
                continue;
            if (nx === px && ny === py) 
                continue;
            if (visited[nx][ny]) 
                return true;
            if (dfs(nx, ny, x, y)) 
                return true;
        }
        return false;
    };
    
    for (let i = 0; i < m; i++) {
        for (let j = 0; j < n; j++) {
            if (!visited[i][j] && dfs(i, j, -1, -1)) {
                return true;
            }
        }
    }
    return false;
};