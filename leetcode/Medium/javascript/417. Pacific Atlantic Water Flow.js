/*
https://leetcode.com/problems/pacific-atlantic-water-flow/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

/**
 * @param {number[][]} heights
 * @return {number[][]}
 */
var pacificAtlantic = function(heights) {
    const m = heights.length, n = heights[0].length;
    const pac = Array.from({ length: m }, () => Array(n).fill(false));
    const atl = Array.from({ length: m }, () => Array(n).fill(false));
    const dirs = [[1,0],[-1,0],[0,1],[0,-1]];

    const dfs = (x, y, visited) => {
        visited[x][y] = true;
        for (const [dx, dy] of dirs) {
            const nx = x + dx, ny = y + dy;
            if (nx < 0 || nx >= m || ny < 0 || ny >= n) continue;
            if (visited[nx][ny] || heights[nx][ny] < heights[x][y]) continue;
            dfs(nx, ny, visited);
        }
    };

    for (let i = 0; i < m; i++) {
        dfs(i, 0, pac);
        dfs(i, n - 1, atl);
    }
    for (let j = 0; j < n; j++) {
        dfs(0, j, pac);
        dfs(m - 1, j, atl);
    }

    const res = [];
    for (let i = 0; i < m; i++)
        for (let j = 0; j < n; j++)
            if (pac[i][j] && atl[i][j]) res.push([i, j]);
    return res;
};

/*
''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/