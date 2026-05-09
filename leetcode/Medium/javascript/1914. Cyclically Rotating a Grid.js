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
 * Циклически сдвигает каждый слой матрицы на k шагов против часовой стрелки.
 * @param {number[][]} grid - Исходная матрица m x n (m и n - чётные).
 * @param {number} k - Количество циклических сдвигов.
 * @return {number[][]} Матрица после выполнения k циклических сдвигов для каждого слоя.
 */
var rotateGrid = function(grid, k) {
    const m = grid.length;
    const n = grid[0].length;
    const layers = Math.min(m, n) / 2;

    for (let layer = 0; layer < layers; layer++) {
        const elements = [];

        // Верхняя строка
        for (let col = layer; col < n - layer; col++)
            elements.push(grid[layer][col]);
        // Правый столбец
        for (let row = layer + 1; row < m - layer; row++)
            elements.push(grid[row][n - 1 - layer]);
        // Нижняя строка
        if (m - 1 - layer > layer)
            for (let col = n - 2 - layer; col >= layer; col--)
                elements.push(grid[m - 1 - layer][col]);
        // Левый столбец
        if (n - 1 - layer > layer)
            for (let row = m - 2 - layer; row > layer; row--)
                elements.push(grid[row][layer]);

        const length = elements.length;
        if (length === 0) continue;
        const shift = k % length;

        let idx = 0;
        // Верхняя строка
        for (let col = layer; col < n - layer; col++)
            grid[layer][col] = elements[(shift + idx++) % length];
        // Правый столбец
        for (let row = layer + 1; row < m - layer; row++)
            grid[row][n - 1 - layer] = elements[(shift + idx++) % length];
        // Нижняя строка
        if (m - 1 - layer > layer)
            for (let col = n - 2 - layer; col >= layer; col--)
                grid[m - 1 - layer][col] = elements[(shift + idx++) % length];
        // Левый столбец
        if (n - 1 - layer > layer)
            for (let row = m - 2 - layer; row > layer; row--)
                grid[row][layer] = elements[(shift + idx++) % length];
    }
    return grid;
};