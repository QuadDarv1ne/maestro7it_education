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
 * @param {number} n
 * @return {number}
 */
var concatenatedBinary = function(n) {
    const MOD = 1000000007;
    let ans = 0;
    let bits = 0; // текущая длина двоичного представления числа i

    for (let i = 1; i <= n; i++) {
        // Если i — степень двойки, увеличиваем bits
        if ((i & (i - 1)) === 0) {
            bits++;
        }
        // Конкатенация через умножение (эквивалент сдвига влево) и сложение
        // 1 << bits безопасно, так как bits ≤ 17 < 30
        ans = (ans * (1 << bits) + i) % MOD;
    }
    return ans;
};