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
 * Подсчёт количества зигзагообразных массивов.
 * 
 * Использует тип BigInt для предотвращения потери точности при умножении больших чисел.
 * Выполняет быстрое возведение матрицы в степень с трекингом вектора.
 * 
 * @param {number} n - Длина массива
 * @param {number} l - Левая граница диапазона
 * @param {number} r - Правая граница диапазона
 * @return {number} Количество зигзагообразных массивов по модулю 10^9+7
 */
var zigZagArrays = function(n, l, r) {
    const MOD = 10n**9n + 7n;
    let m = r - l + 1;
    if (n === 1) return Number(m);
    
    let size = 2 * m;
    let M = Array.from({length: size}, () => Array(size).fill(0n));
    
    for (let i = 0; i < m; i++) {
        for (let j = i + 1; j < m; j++) M[i][m + j] = 1n;
        for (let j = 0; j < i; j++) M[m + i][j] = 1n;
    }
    
    let V = Array(size).fill(1n);
    let power = n - 1;
    
    while (power > 0) {
        if ((power & 1) === 1) {
            V = matVecMul(M, V, MOD);
        }
        M = matMul(M, M, MOD);
        power >>= 1;
    }
    
    let ans = 0n;
    for (let x of V) ans = (ans + x) % MOD;
    return Number(ans);
};

function matMul(A, B, MOD) {
    let n = A.length;
    let C = Array.from({length: n}, () => Array(n).fill(0n));
    for (let i = 0; i < n; i++) {
        for (let k = 0; k < n; k++) {
            if (A[i][k] !== 0n) {
                for (let j = 0; j < n; j++) {
                    C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % MOD;
                }
            }
        }
    }
    return C;
}

function matVecMul(M, V, MOD) {
    let n = M.length;
    let res = Array(n).fill(0n);
    for (let i = 0; i < n; i++) {
        let sum = 0n;
        for (let j = 0; j < n; j++) {
            sum = (sum + M[i][j] * V[j]) % MOD;
        }
        res[i] = sum;
    }
    return res;
}