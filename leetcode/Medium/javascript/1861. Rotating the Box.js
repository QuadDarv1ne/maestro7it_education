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
 * Поворачивает матрицу и применяет гравитацию к камням.
 *
 * @param {character[][]} boxGrid - Исходная матрица (боковой вид коробки).
 *        '#' обозначает камень, '*' - препятствие, '.' - пустоту.
 * @return {character[][]} - Матрица после поворота на 90 градусов по часовой
 *         стрелке и применения гравитации.
 */
var rotateTheBox = function(boxGrid) {
    const m = boxGrid.length;
    const n = boxGrid[0].length;

    // Применяем гравитацию в исходной матрице (сдвигаем камни вправо)
    for (let i = 0; i < m; i++) {
        let emptyPos = n - 1;
        for (let j = n - 1; j >= 0; j--) {
            if (boxGrid[i][j] === '*') {
                emptyPos = j - 1;
            } else if (boxGrid[i][j] === '#') {
                // Меняем камень с пустой клеткой
                [boxGrid[i][j], boxGrid[i][emptyPos]] = [boxGrid[i][emptyPos], boxGrid[i][j]];
                emptyPos--;
            }
        }
    }

    // Создаем новую повернутую матрицу (n x m)
    const rotatedBox = Array.from({ length: n }, () => new Array(m));

    // Поворачиваем на 90 градусов по часовой стрелке
    for (let i = 0; i < m; i++) {
        for (let j = 0; j < n; j++) {
            rotatedBox[j][m - 1 - i] = boxGrid[i][j];
        }
    }

    return rotatedBox;
};