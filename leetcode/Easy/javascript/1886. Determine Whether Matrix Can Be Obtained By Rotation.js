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
 * @param {number[][]} mat
 * @param {number[][]} target
 * @return {boolean}
 */
var findRotation = function(mat, target) {
    const n = mat.length;
    
    // Функция для поворота матрицы на 90° по часовой стрелке
    const rotate90 = (matrix) => {
        // Транспонирование
        for (let i = 0; i < n; i++) {
            for (let j = i + 1; j < n; j++) {
                [matrix[i][j], matrix[j][i]] = [matrix[j][i], matrix[i][j]];
            }
        }
        // Отражение каждой строки
        for (let i = 0; i < n; i++) {
            matrix[i].reverse();
        }
    };
    
    // Проверяем 4 возможных поворота
    for (let rot = 0; rot < 4; rot++) {
        if (JSON.stringify(mat) === JSON.stringify(target)) {
            return true;
        }
        rotate90(mat);
    }
    
    return false;
};