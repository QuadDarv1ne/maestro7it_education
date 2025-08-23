/**
 * https://leetcode.com/problems/find-the-minimum-area-to-cover-all-ones-ii/description/?envType=daily-question&envId=2025-08-23
 */

/**
 * Находит минимальную суммарную площадь трёх непересекающихся прямоугольников,
 * покрывающих все единицы в бинарной матрице.
 */
var minimumSum = function(grid) {
    const m = grid.length, n = grid[0].length;
    const INF = m * n + 5;
    let ans = INF;

    function area(r1, r2, c1, c2) {
        let rmin = 1e9, rmax = -1e9, cmin = 1e9, cmax = -1e9;
        for (let r = r1; r <= r2; ++r) {
            for (let c = c1; c <= c2; ++c) {
                if (grid[r][c] === 1) {
                    if (r < rmin) rmin = r;
                    if (r > rmax) rmax = r;
                    if (c < cmin) cmin = c;
                    if (c > cmax) cmax = c;
                }
            }
        }
        if (rmin === 1e9) return 0;
        return (rmax - rmin + 1) * (cmax - cmin + 1);
    }

    // три горизонтали
    for (let i = 1; i < m; ++i) {
        for (let j = i+1; j < m; ++j) {
            const a = area(0, i-1, 0, n-1);
            const b = area(i, j-1, 0, n-1);
            const c = area(j, m-1, 0, n-1);
            ans = Math.min(ans, a + b + c);
        }
    }

    // три вертикали
    for (let i = 1; i < n; ++i) {
        for (let j = i+1; j < n; ++j) {
            const a = area(0, m-1, 0, i-1);
            const b = area(0, m-1, i, j-1);
            const c = area(0, m-1, j, n-1);
            ans = Math.min(ans, a + b + c);
        }
    }

    // горизонтальный + вертикальный
    for (let i = 0; i < m-1; ++i) {
        for (let j = 0; j < n-1; ++j) {
            const topLeft = area(0, i, 0, j);
            const topRight = area(0, i, j+1, n-1);
            const bottom = area(i+1, m-1, 0, n-1);
            ans = Math.min(ans, topLeft + topRight + bottom);

            const top = area(0, i, 0, n-1);
            const bottomLeft = area(i+1, m-1, 0, j);
            const bottomRight = area(i+1, m-1, j+1, n-1);
            ans = Math.min(ans, top + bottomLeft + bottomRight);
        }
    }

    // вертикальный + горизонтальный
    for (let i = 0; i < n-1; ++i) {
        for (let j = 0; j < m-1; ++j) {
            const leftTop = area(0, j, 0, i);
            const leftBottom = area(j+1, m-1, 0, i);
            const right = area(0, m-1, i+1, n-1);
            ans = Math.min(ans, leftTop + leftBottom + right);

            const left = area(0, m-1, 0, i);
            const rightTop = area(0, j, i+1, n-1);
            const rightBottom = area(j+1, m-1, i+1, n-1);
            ans = Math.min(ans, left + rightTop + rightBottom);
        }
    }

    return (ans === INF) ? 0 : ans;
};

/*
''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/