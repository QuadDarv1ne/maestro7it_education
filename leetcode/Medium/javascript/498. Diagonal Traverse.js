/**
 * https://leetcode.com/problems/diagonal-traverse/description/
 */

/**
 * Возвращает элементы матрицы в порядке диагонального обхода (зигзаг).
 *
 * Алгоритм:
 * 1. Начинаем с (0,0).
 * 2. Двигаемся вверх-вправо или вниз-влево.
 * 3. Меняем направление на границах.
 * 4. Повторяем, пока не соберем все элементы.
 *
 * Пример:
 * Ввод: [[1,2,3],[4,5,6],[7,8,9]]
 * Вывод: [1,2,4,7,5,3,6,8,9]
 *
 * @param {number[][]} mat - матрица чисел
 * @return {number[]} массив чисел в диагональном порядке
 */
var findDiagonalOrder = function(mat) {
    if (!mat || !mat.length) return [];
    let m = mat.length, n = mat[0].length;
    let result = [];
    let row = 0, col = 0, direction = 1;

    while (result.length < m * n) {
        result.push(mat[row][col]);
        if (direction === 1) { // вверх-вправо
            if (col === n - 1) { row++; direction = -1; }
            else if (row === 0) { col++; direction = -1; }
            else { row--; col++; }
        } else { // вниз-влево
            if (row === m - 1) { col++; direction = 1; }
            else if (col === 0) { row++; direction = 1; }
            else { row++; col--; }
        }
    }
    return result;
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