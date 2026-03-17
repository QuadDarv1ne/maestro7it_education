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
 * @param {number[][]} matrix
 * @return {number}
 */
var largestSubmatrix = function(matrix) {
    if (!matrix || matrix.length === 0) return 0;

    const m = matrix.length;
    const n = matrix[0].length;
    let maxArea = 0;
    // heights[j] будет хранить количество последовательных 1 в столбце j до текущей строки
    let heights = new Array(n).fill(0);

    for (let i = 0; i < m; i++) {
        // Обновляем высоты для текущей строки
        for (let j = 0; j < n; j++) {
            if (matrix[i][j] === 1) {
                heights[j] += 1;
            } else {
                heights[j] = 0;
            }
        }

        // Создаем копию heights для текущей строки, чтобы отсортировать
        let currentHeights = [...heights];
        currentHeights.sort((a, b) => b - a);

        // Вычисляем максимальную площадь для этой строки
        for (let j = 0; j < n; j++) {
            // currentHeights[j] - это минимальная высота в прямоугольнике,
            // а (j + 1) столбцов имеют высоту >= currentHeights[j]
            maxArea = Math.max(maxArea, currentHeights[j] * (j + 1));
        }
    }

    return maxArea;
};