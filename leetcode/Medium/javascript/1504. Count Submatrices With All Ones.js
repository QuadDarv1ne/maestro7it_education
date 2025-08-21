/**
 * https://leetcode.com/problems/count-submatrices-with-all-ones/description/?envType=daily-question&envId=2025-08-21
 */

/**
 * Подсчёт количества подматриц, состоящих только из единиц.
 * @param {number[][]} mat - бинарная матрица
 * @return {number}
 */
var numSubmat = function(mat) {
    let m = mat.length, n = mat[0].length;
    let continuous = Array.from({length: m}, () => Array(n).fill(0));

    // Подсчёт подряд идущих единиц
    for (let i = 0; i < m; i++) {
        for (let j = 0; j < n; j++) {
            if (mat[i][j] === 1) {
                continuous[i][j] = (j > 0 ? continuous[i][j - 1] : 0) + 1;
            }
        }
    }

    let ans = 0;
    // Подсчёт количества подматриц
    for (let i = 0; i < m; i++) {
        for (let j = 0; j < n; j++) {
            let minWidth = Infinity;
            for (let k = i; k >= 0; k--) {
                minWidth = Math.min(minWidth, continuous[k][j]);
                ans += minWidth;
            }
        }
    }
    return ans;
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