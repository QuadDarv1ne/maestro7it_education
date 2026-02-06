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

var calculateMinimumHP = function(dungeon) {
    /**
     * Вычисляет минимальное начальное здоровье рыцаря для спасения принцессы.
     * Использует обратное динамическое программирование (от конца к началу).
     * 
     * Сложность по времени: O(m * n)
     * Сложность по памяти: O(m * n)
     */
    const m = dungeon.length;
    const n = dungeon[0].length;
    
    // Создаём DP таблицу с дополнительной строкой и столбцом
    const dp = Array(m + 1).fill(0).map(() => Array(n + 1).fill(Infinity));
    
    // Базовые случаи
    dp[m - 1][n] = 1;
    dp[m][n - 1] = 1;
    
    // Заполняем таблицу от конца к началу
    for (let i = m - 1; i >= 0; i--) {
        for (let j = n - 1; j >= 0; j--) {
            // Минимальное HP нужное для следующего хода
            const minHpNext = Math.min(dp[i + 1][j], dp[i][j + 1]);
            
            // HP нужное для текущей клетки
            dp[i][j] = Math.max(1, minHpNext - dungeon[i][j]);
        }
    }
    
    return dp[0][0];
};