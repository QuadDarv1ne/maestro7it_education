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
 * Находит количество стабильных бинарных массивов.
 * 
 * @param {number} zero - Требуемое количество нулей в массиве
 * @param {number} one - Требуемое количество единиц в массиве
 * @param {number} limit - Максимальная длина подряд идущих одинаковых элементов
 * @return {number} Количество стабильных массивов по модулю 10^9+7
 * 
 * @description
 * Алгоритм: Динамическое программирование с трёхмерным состоянием.
 * 
 * Состояние ДП:
 *   dp[i][j][k] — количество стабильных массивов с:
 *     - i нулями
 *     - j единицами
 *     - последний элемент равен k (0 или 1)
 * 
 * Формулы перехода:
 *   - При добавлении 0:
 *     dp[i][j][0] = dp[i-1][j][0] + dp[i-1][j][1] 
 *                   - (i > limit ? dp[i-limit-1][j][1] : 0)
 *   - При добавлении 1: аналогично с заменой 0 ↔ 1
 * 
 * Базовые случаи:
 *   - Массивы из одних нулей длиной 1..limit: dp[i][0][0] = 1
 *   - Массивы из одних единиц длиной 1..limit: dp[0][j][1] = 1
 * 
 * Сложность:
 *   Время: O(zero × one)
 *   Память: O(zero × one)
 * 
 * @example
 * // Вход: zero = 1, one = 1, limit = 2
 * // Выход: 2 (массивы [0,1] и [1,0])
 */
var numberOfStableArrays = function(zero, one, limit) {
    const MOD = 1_000_000_007;
    
    // dp[i][j][k]: i нулей, j единиц, последний бит = k
    const dp = Array.from({ length: zero + 1 }, () =>
        Array.from({ length: one + 1 }, () => [0, 0])
    );
    
    // Базовые случаи
    for (let i = 0; i <= Math.min(zero, limit); i++) {
        dp[i][0][0] = 1;
    }
    for (let j = 0; j <= Math.min(one, limit); j++) {
        dp[0][j][1] = 1;
    }
    
    // Заполнение таблицы ДП
    for (let i = 1; i <= zero; i++) {
        for (let j = 1; j <= one; j++) {
            // Добавляем 0 в конец
            dp[i][j][0] = (
                dp[i - 1][j][0] + 
                dp[i - 1][j][1] - 
                (i - limit >= 1 ? dp[i - limit - 1][j][1] : 0) + 
                MOD
            ) % MOD;
            
            // Добавляем 1 в конец
            dp[i][j][1] = (
                dp[i][j - 1][0] + 
                dp[i][j - 1][1] - 
                (j - limit >= 1 ? dp[i][j - limit - 1][0] : 0) + 
                MOD
            ) % MOD;
        }
    }
    
    return (dp[zero][one][0] + dp[zero][one][1]) % MOD;
};