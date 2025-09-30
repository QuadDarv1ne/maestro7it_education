/**
 * https://leetcode.com/problems/triangle/description/?envType=daily-question&envId=2025-09-25
 */

/**
 * Вычисляет минимальную сумму пути от вершины до основания треугольника.
 *
 * @param {number[][]} triangle — треугольник, массив массивов
 * @return {number} минимальная сумма пути
 */
var minimumTotal = function(triangle) {
    const n = triangle.length;
    if (n === 0) return 0;
    // модифицируем triangle in-place
    for (let i = n - 2; i >= 0; i--) {
        for (let j = 0; j <= i; j++) {
            const belowLeft = triangle[i+1][j];
            const belowRight = triangle[i+1][j+1];
            triangle[i][j] += Math.min(belowLeft, belowRight);
        }
    }
    return triangle[0][0];
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