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
 * @return {number[]}
 */
var getBiggestThree = function(grid) {
    const m = grid.length;
    const n = grid[0].length;
    const sums = new Set(); // Используем Set для уникальности

    for (let i = 0; i < m; i++) {
        for (let j = 0; j < n; j++) {
            // Ромб размера 1
            sums.add(grid[i][j]);

            const maxK = Math.min(i, m - 1 - i, j, n - 1 - j) + 1;
            for (let k = 2; k <= maxK; k++) {
                let total = 0;
                const r1 = i - (k - 1), c1 = j;
                const r2 = i, c2 = j + (k - 1);
                const r3 = i + (k - 1), c3 = j;
                const r4 = i, c4 = j - (k - 1);

                // Верх -> Право
                for (let s = 0; s < k - 1; s++) total += grid[r1 + s][c1 + s];
                // Право -> Низ
                for (let s = 0; s < k - 1; s++) total += grid[r2 + s][c2 - s];
                // Низ -> Лево
                for (let s = 0; s < k - 1; s++) total += grid[r3 - s][c3 - s];
                // Лево -> Верх
                for (let s = 0; s < k - 1; s++) total += grid[r4 - s][c4 + s];

                sums.add(total);
            }
        }
    }

    // Преобразуем Set в массив, сортируем по убыванию и берем первые 3
    return Array.from(sums).sort((a, b) => b - a).slice(0, 3);
};