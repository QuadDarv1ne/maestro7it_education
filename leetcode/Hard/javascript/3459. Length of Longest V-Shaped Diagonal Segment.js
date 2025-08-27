/**
 * https://leetcode.com/problems/length-of-longest-v-shaped-diagonal-segment/description/?envType=daily-question&envId=2025-08-27
 */

/**
 * lenOfVDiagonal
 *
 * Вычисляет длину самого длинного V-образного диагонального сегмента в матрице.
 *
 * Условия сегмента:
 * 1. Начало сегмента всегда с числа 1.
 * 2. Далее значения идут по шаблону: 2 → 0 → 2 → 0 → ...
 * 3. Движение только по диагоналям: ↘, ↙, ↖, ↗.
 * 4. Разрешён ровно один поворот на 90° по часовой стрелке.
 * 5. Если сегмента нет, возвращается 0.
 *
 * @param {number[][]} grid - Входная матрица чисел.
 * @returns {number} Длина самого длинного V-образного диагонального сегмента.
 */
let lenOfVDiagonal = function (grid) {
    const n = grid.length;
    const m = grid[0].length;
    const DIRS = [[1, 1], [1, -1], [-1, -1], [-1, 1]];
    const memo = Array.from({ length: n }, () => Array.from({ length: m }, () => Array(1 << 3).fill(0)));

    let ans = 0;

    for (let i = 0; i < n; i++) {
        for (let j = 0; j < m; j++) {
            if (grid[i][j] !== 1) continue;

            const maxs = [n - i, j + 1, i + 1, m - j];

            for (let k = 0; k < 4; k++) {
                if (maxs[k] > ans) {
                    ans = Math.max(ans, dfs(i, j, k, 1, 2) + 1);
                }
            }
        }
    }

    return ans;

    /**
     * Рекурсивная функция DFS для поиска V-образного сегмента
     *
     * @param {number} i - Текущая координата X.
     * @param {number} j - Текущая координата Y.
     * @param {number} k - Индекс текущего направления диагонали.
     * @param {number} canTurn - Флаг, разрешён ли поворот (1 или 0).
     * @param {number} target - Ожидаемое значение в текущей клетке.
     * @returns {number} Длина сегмента от текущей позиции.
     */
    function dfs(i, j, k, canTurn, target) {
        i += DIRS[k][0];
        j += DIRS[k][1];

        if (i < 0 || i >= n || j < 0 || j >= m || grid[i][j] !== target) return 0;

        const mask = (k << 1) | canTurn;
        if (memo[i][j][mask] > 0) return memo[i][j][mask];

        let res = dfs(i, j, k, canTurn, 2 - target);

        if (canTurn === 1) {
            const maxs = [n - i - 1, j, i, m - j - 1];
            const nk = (k + 1) % 4;

            if (maxs[nk] > res) {
                res = Math.max(res, dfs(i, j, nk, 0, 2 - target));
            }
        }

        return (memo[i][j][mask] = res + 1);
    }
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