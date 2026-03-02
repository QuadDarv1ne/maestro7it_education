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
 * @return {number}
 */
var minSwaps = function(grid) {
    const n = grid.length;
    // Вычисляем количество нулей в конце каждой строки
    const trailing = [];
    for (let i = 0; i < n; i++) {
        let cnt = 0;
        for (let j = n - 1; j >= 0; j--) {
            if (grid[i][j] === 0) {
                cnt++;
            } else {
                break;
            }
        }
        trailing.push(cnt);
    }
    
    let ans = 0;
    for (let i = 0; i < n; i++) {
        const required = n - 1 - i;
        // ищем строку с требуемым количеством нулей, начиная с i
        let j = i;
        while (j < n && trailing[j] < required) {
            j++;
        }
        if (j === n) return -1;
        // добавляем количество свопов
        ans += j - i;
        // перемещаем найденный элемент на позицию i (сдвигаем массив)
        const val = trailing[j];
        trailing.splice(j, 1);
        trailing.splice(i, 0, val);
    }
    return ans;
};